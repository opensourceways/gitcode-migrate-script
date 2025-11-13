import base64
import subprocess
import time
import requests
import logging

from config import GiteeV8Token, GiteePWD, StrReadmeAddContent, DirName, Cookie, X_Csrf_Token

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

SUC_StatusCode = [200, 201, 204]


# ReadmeAddContent = bytes(StrReadmeAddContent, encoding="utf8")


class GiteeApp:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 ):
        self.access_token = access_token
        self.owner = owner
        self.enterprise = enterprise
        self.base_v5_url = "https://gitee.com/api/v5/"

        self.enterprise_id = self.get_enterprise_id(self.base_v5_url, enterprise, access_token)

    @classmethod
    def get_enterprise_id(cls, base_url, enterprise, token) -> int:
        """
        获取企业id, 注意 enterprise 和 owner 并不等价
        :param base_url:
        :param enterprise:
        :param token:
        :return:
        """
        logging.info(f"get {enterprise} id...")
        url = f"{base_url}enterprises/{enterprise}?access_token={token}"
        response = requests.get(url)
        return response.json().get("id")

    def get_repo_id(self, repo):
        """
        获取代码仓id
        :param repo:
        :return:
        """
        url = f"{self.base_v5_url}repos/{self.owner}/{repo}?access_token={self.access_token}"
        response = requests.get(url)
        return response.json().get("id")

    def get_repos(self) -> list[str]:
        """
        获取 self.owner 所有代码仓
        :return:
        """
        logging.info(f"Get {self.owner} repos...")
        url = f"{self.base_v5_url}orgs/{self.owner}/repos?access_token={self.access_token}"
        page, per_page = 1, 100
        params = dict(per_page=per_page, page=page)
        repos = []
        while True:
            response = requests.get(url, params=params)
            cnt = response.headers.get("total_count")
            _repos = response.json()
            for _repo in _repos:
                repos.append(_repo.get("full_name"))

            if page * per_page > int(cnt):
                break
            page += 1
            params.update(page=page)

        return list(set(repos))

    def lock_repo(self, repo: str):
        logging.info(f"lock repo: {repo}")
        repo_id = self.get_repo_id(repo)
        url = f"https://api.gitee.com/enterprises/{self.enterprise_id}/projects/{repo_id}/status"
        params = dict(access_token=GiteeV8Token,
                      status=1,  # 0：开始，1：暂停，2：关闭
                      password=GiteePWD,
                      validate_type='password'
                      )
        response = requests.put(url, params=params)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"lock {repo} failure, {response.text}")

    def get_repo_issue(self, repo):
        """
        获取代码仓repo 的所有issue
        :param repo:
        :return:
        """
        url = f"{self.base_v5_url}/repos/{self.owner}/{repo}/issues"
        page = 1
        params = {
            "access_token": self.access_token,
            "state": "all",
            "page": page,
            "per_page": 50,
        }
        result = []
        while True:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                logging.info("gitee times limit...")
                time.sleep(60)

            for item in response.json():
                result.append([
                    repo, item.get("number"),
                    item.get("title"),
                    item.get("issue_type"),
                    item.get("state"),
                    item.get("issue_state"),
                    item.get("user", {}).get("login")
                ])
            if int(response.headers.get("total_page")) <= page:
                break
            page += 1
            params.update(page=page)
        return result

    def get_readme_content(self, repo):
        """
        获取readme 内容
        :param repo:
        :return:
        """
        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/raw/README.md?access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"get repo {repo} readme fail, {response.text}")
        content = response.content
        return content

    def get_readme_sha(self, repo):
        """获取readme sha 值"""
        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/readme?access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"get repo {repo} sha fail: {response.text}")
        return response.json().get("sha")

    def update_readme(self, repo):
        """
        在 readme 上新增迁移公告
        :param repo:
        :return:
        """
        content = self.get_readme_content(repo)
        sha = self.get_readme_sha(repo)

        _insert = bytes(StrReadmeAddContent.format(owner=self.owner, repo=repo), encoding="utf8")

        content = _insert + content

        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/contents/README.md"
        params = {
            "access_token": self.access_token,
            "content": base64.b64encode(content),
            "sha": sha,
            "message": "update README.md"
        }

        response = requests.put(url, params=params)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"modify {repo} readme fail, {response.text}")

    def get_readme_file(self, repo: str) -> dict:
        """
        https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepoReadme
        获取readme 路径
        :return:
        """
        url = f"https://gitee.com/api/v5/repos/{self.owner}/{repo}/readme?access_token={self.access_token}"
        response = requests.get(url)
        return response.json()

    def update_readme_sh(self, repo: str):
        """
        通过git 命令更新readme
        :return:
        """
        readme_url = self.get_readme_file(repo).get("url")
        logging.info(f"{self.owner}/{repo} readme path: {readme_url}")

        if readme_url:
            readme_lst = readme_url.split("contents")[-1].split("/")[1:]
            file_name = readme_lst[-1]
            path = "/".join(readme_lst[:-1])
            ret = subprocess.call(["../tools/insert_to_readme.sh", repo, self.owner, file_name, path])
            if ret != 0:
                logging.error(f"update {self.owner}/{repo} README fail...")
        else:
            self.new_file_tips(repo, "README.md")

    def new_file_tips(self, repo, dir_name: str = DirName):
        """
        新建文件夹, 显示迁移公告
        :param dir_name:
        :param repo:
        :return:
        """
        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/contents/{dir_name}"
        _insert = bytes(StrReadmeAddContent.format(owner=self.owner, repo=repo), encoding="utf8")
        params = {
            "access_token": self.access_token,
            "content": base64.b64encode(_insert),
            "message": "update README.md"
        }
        response = requests.post(url, params=params)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"new {repo} dir fail, {response.text}")

    def update_repo_settings(self, repo):
        """
        禁用在线编辑、提交pr、新增issue
        :param repo:
        :return:
        """
        url = f"https://gitee.com/{self.owner}/{repo}"
        payload = {
            "online_edit_enabled": 0,
            "project[readonly_issue]": 1,
            "project[readonly_pull_request]": 1,
        }
        headers = {
            "X-Csrf-Token": X_Csrf_Token,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": Cookie
        }
        response = requests.put(url, data=payload, headers=headers)
        if response.status_code not in SUC_StatusCode:
            logging.error(f"update repo {repo} fail, {response.text}")

    def get_repo_webhook(self, repo: str):
        """
        获取代码仓所有webhook
        :param repo:
        :return:
        """
        _repo = repo.split("/")
        organization, repo = _repo if len(_repo) == 2 else (None, _repo[0])

        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/hooks?access_token={self.access_token}"
        page = 1
        result = []
        while True:
            response = requests.get(f"{url}&page={page}&per_page=100")
            if response.status_code != 200:
                break
            total_page = int(response.headers.get("total_page"))
            for ele in response.json():
                result.append([organization,
                               repo,
                               ele.get("url"),
                               ele.get("password"),
                               ele.get("push_events"),
                               ele.get("tag_push_events"),
                               ele.get("issues_events"),
                               ele.get("note_events"),
                               ele.get("merge_requests_events"),
                               ])
            if page >= total_page:
                break

            page += 1
        return list(result)

    def get_user_email(self, login_id: str):
        """
        通过gitee id获取用户邮箱（只有设置公开的邮箱才能获取到）
        :param login_id:
        :return:
        """
        url = f"{self.base_v5_url}users/{login_id}?access_token={self.access_token}"
        response = requests.get(url)

        if response.status_code != 200:
            return
        data = response.json()
        return data.get("email")

    def get_repo_members(self, repo: str) -> list[dict]:
        """
        获取代码仓成员
        :param repo:
        :return:
        """
        url = f"{self.base_v5_url}repos/{self.owner}/{repo}/collaborators"
        params = {
            "access_token": self.access_token,
            "per_page": 100,
        }
        page = 1
        res = []
        while True:
            params.update(page=page)
            response = requests.get(url, params=params)

            total_page = response.headers.get("total_page")
            for item in response.json():
                res.append({
                    "repo": repo,
                    "login_id": item.get("login"),
                    "name": item.get("name")
                })

            if page >= int(total_page):
                break

            page += 1
        return res

    def get_enterprise_members(self, v8_token: str):
        """
        获取企业成员
        :return:
        """
        url = f"https://api.gitee.com/enterprises/{self.enterprise_id}/members"
        params = {
            "access_token": v8_token,
            "per_page": 100,
        }
        page = 1
        res = {}
        while True:
            params.update(page=page)
            response = requests.get(url, params=params)
            total_count = response.json().get("total_count")

            for item in response.json().get("data"):
                res.update({
                    item.get("id"): {
                        "username": item.get("username"),
                        "name": item.get("name"),
                        "remark": item.get("remark"),
                        "email": item.get("email"),
                        "phone": item.get("phone")
                    }
                })

            if page * 100 > total_count:
                break
            page += 1

        return res

    def clear_enterprise_user(self, username: str):
        """
        清除企业成员
        :param username
        :return:
        """
        url = f"https://gitee.com/api/v5/enterprises/{self.enterprise}/members/{username}?access_token={self.access_token}"
        response = requests.delete(url)
        if response.status_code not in [200, 201, 204]:
            logging.error(f"delete user {username} from enterprise {self.enterprise} failed...")

    def get_repo_branches_attr(self, repo: str, v8_token: str) -> list:
        """
        https://gitee.com/api/v8/swagger#/getEnterpriseIdProjectsProjectIdBranches
        获取代码仓分支属性
        :param v8_token:
        :param repo:
        :return:
        """
        project_id = self.get_repo_id(repo)
        url = f"https://api.gitee.com/enterprises/{self.enterprise_id}/projects/{project_id}/branches"
        params = {
            "access_token": v8_token,
            "per_page": 100,
        }
        page = 1
        branches = []

        while True:
            params.update(page=page)
            response = requests.get(url, params=params)
            result = response.json()

            total_count = result.get("total_count")

            for item in result.get("data"):
                branches.append({
                    "name": item.get("name"),
                    "branch_type": item.get("branch_type"),
                    "protection_rule": item.get("protection_rule")
                })

            if page * 100 >= total_count:
                break

            page += 1

        return branches

    def get_repo_info(self,
                      repo: str,
                      owner: str = None
                      ):
        """
        https://gitee.com/api/v5/swagger#/getV5ReposOwnerRepo
        :param repo:
        :param owner:
        :return:
        """
        if owner is None:
            owner = self.owner

        url = f"{self.base_v5_url}repos/{owner}/{repo}?access_token={self.access_token}"

        response = requests.get(url)

        if response.status_code not in SUC_StatusCode:
            logging.error(f"Get {owner}/{repo} failed...")
            logging.error(response.text)

        return response.json()
