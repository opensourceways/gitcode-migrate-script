import logging
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")
ROLE_CONFIG = {}


class GitcodeApp:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        self.base_url = "https://api.gitcode.com/api/v5"
        self.base_v8_url = "https://api.gitcode.com/api/v8"

        self.enterprise_id = self.get_enterprise_id()

    def get_enterprise_id(self):
        """
        获取企业id
        :return:
        """
        url = f"{self.base_v8_url}/org/{self.owner}/enterprise?access_token={self.access_token}"
        response = requests.get(url)
        return response.json().get("id")

    def check_user_exist(self, username: str) -> bool:
        """
        https://docs.gitcode.com/docs/apis/get-api-v-5-users-username
        检测该用户是否存在
        :param username:
        :return:
        """
        url = f"{self.base_url}/users/{username}?access_token={self.access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        return False

    def invite_to_enterprise(self, username: str, role_id: str):
        """
        https://docs.gitcode.com/docs/apis/post-api-v-8-enterprises-enterprise-memberships-username
        :param role_id: 角色uuid
        :param username:
        :return:
        """
        if not self.check_user_exist(username):
            logging.error(f"user: {username} not exist...")

        url = f"{self.base_v8_url}/enterprises/{self.enterprise_id}/memberships/{username}"
        url = f"{url}?access_token={self.access_token}"
        body = dict(permission="customized", role_id=role_id)

        response = requests.post(url=url, json=body)
        if response.status_code != 200:
            logging.error(f"invite user: {username}  to enterprise failed: {response.text}")

    def invite_to_organization(self, username: str, role: str, role_id: str = None):
        """
        https://docs.gitcode.com/docs/apis/post-api-v-5-orgs-org-memberships-username
        邀请成员至组织
        :param role_id:
        :param username:
        :param role:
        :return:
        """
        if not self.check_user_exist(username):
            logging.error(f"user: {username} not exist...")

        url = f"{self.base_url}/orgs/{self.owner}/memberships/{username}?access_token={self.access_token}"
        role_id = role_id or ROLE_CONFIG.get(role, None)

        data = dict(permission="push")
        if role in ["管理员", "admin"]:
            data = dict(permission="admin")
        elif role_id:
            data.update(permission="customized", role_id=role_id)

        response = requests.post(url=url, json=data)
        if response.status_code != 200:
            logging.error(f"invite user: {username}  to org failed: {response.text}")

    def invite_to_repo(self, username: str, repo: str, role: str):
        """
        https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-collaborators-username
        邀请成员至代码仓
        :param username:
        :param repo:
        :param role:
        :return:
        """
        if not self.check_user_exist(username):
            logging.error(f"user: {username} not exist...")

        url = f"{self.base_url}/repos/{self.owner}/{repo}/collaborators/{username}?access_token={self.access_token}"

        permission = "push"
        if role in ["管理员", "admin"]:
            permission = "admin"
        response = requests.put(url=url, json=dict(permission=role))

        if response.status_code != 200:
            logging.error(f"invite user: {username} to repo failed: {response.text}")

    def get_repo_webhooks(self, repo):
        """
        读取gitcode webhooks
        :param repo:
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/hooks"
        params = dict(access_token=self.access_token,
                      page=1,
                      per_page=100
                      )

        response = requests.get(url, params=params)

        result = []
        for item in response.json():
            result.append({
                "url": item.get("url"),
                "encryption_type": "",
                "password": item.get("password"),
                "push_events": item.get("push_events"),
                "tag_push_events": item.get("tag_push_events"),
                "issues_events": item.get("issues_events"),
                "note_events": item.get("note_events"),
                "merge_requests_events": item.get("merge_requests_events"),
            })
        return result

    def add_repo_webhook(self,
                         repo: str,
                         url: str,
                         password: str,
                         push_events: str,
                         tag_push_events: str,
                         issues_events: str,
                         note_events: str,
                         merge_requests_events: str,
                         **kwargs
                         ):
        api = f"{self.base_url}/repos/{self.owner}/{repo}/hooks?access_token={self.access_token}"
        body = {
            "url": url,
            "encryption_type": "",
            "password": password,
            "push_events": push_events,
            "tag_push_events": tag_push_events,
            "issues_events": issues_events,
            "note_events": note_events,
            "merge_requests_events": merge_requests_events,
        }

        response = requests.post(api, data=body)

        if response.status_code != 200:
            logging.info(response.text)

    def add_repo_members(self, repo: str, user: str, admin: str):
        url = f"{self.base_url}/repos/{self.owner}/{repo}/collaborators/{user}"
        body = {"permission": "push"}
        if admin.lower() == "true":
            body = {"permission": "admin"}

        response = requests.put(url=f"{url}?access_token={self.access_token}", data=body)

        if response.status_code != 200:
            logging.info(response.text)

    def update_repo_attr(self, repo: str, private: bool = None, default_branch: str = None, description: str = None):
        """
        https://docs.gitcode.com/docs/apis/patch-api-v-5-repos-owner-repo/

        :param description: 项目描述
        :param repo: 需要更改属性的代码仓
        :param private: 仓库公开或私有。（true/false）
        :param default_branch: 默认分支
        :return:
        """
        logging.info(f"update {repo} attr...")
        url = f"{self.base_url}/repos/{self.owner}/{repo}?access_token={self.access_token}"
        data = dict()

        if private is not None:
            data.update(private=private)

        if default_branch is not None:
            data.update(default_branch=default_branch)

        if description is not None:
            data.update(description=description)

        if not data:
            return

        response = requests.patch(url, json=data)
        if response.status_code != 200:
            logging.error(f"error: {response.status_code}, {response.text}")

    def update_repo_setting(self, repo: str,
                            generate_pre_merge_ref: bool = True,
                            forbidden_developer_create_branch: bool = True,
                            forbidden_developer_create_tag: bool = True
                            ):
        """
        https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-repo-settings
        更新仓库设置
        :param forbidden_developer_create_tag:  禁止开发者创建标签
        :param forbidden_developer_create_branch:  禁止开发者创建分支
        :param repo: 需要更改属性的代码仓
        :param generate_pre_merge_ref:   合并请求PR预合并
        :return:
        """
        logging.info(f"update repo {repo} setting...")
        url = f"{self.base_url}/repos/{self.owner}/{repo}/repo_settings?access_token={self.access_token}"
        json = {
            "generate_pre_merge_ref": generate_pre_merge_ref,
            "forbidden_developer_create_branch": forbidden_developer_create_branch,
            "forbidden_developer_create_tag": forbidden_developer_create_tag,
        }
        response = requests.put(url, json=json)
        if response.status_code != 200:
            logging.error(f"error: {response.status_code}, {response.text}")

    def update_pr_settings(self,
                           repo: str,
                           add_notes_after_merged: bool = True,
                           merged_commit_author: str = None,
                           is_allow_lite_merge_request: bool = True,
                           disable_merge_by_self: bool = True,
                           ):
        """
        https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-pull-request-settings
        更新pr属性
        :param disable_merge_by_self: 禁止合入自己创建的合并请求
        :param is_allow_lite_merge_request:  是否启用轻量级 Pull Request
        :param merged_commit_author: 合并模式: 1. 使用 PR 合入者生成 Merge Commit: merged_by 2: 使用 PR 创建者生成 Merge Commit: created_by
        :param add_notes_after_merged:  允许合并请求合并后继续做代码检视和评论
        :param repo:
        :return:
        """
        logging.info(f"update {repo} pr settings...")
        url = f"{self.base_url}/repos/{self.owner}/{repo}/pull_request_settings?access_token={self.access_token}"
        json = {
            "add_notes_after_merged": add_notes_after_merged,
            "is_allow_lite_merge_request": is_allow_lite_merge_request,
            "disable_merge_by_self": disable_merge_by_self
        }

        if merged_commit_author:
            json.update(merged_commit_author=merged_commit_author)

        response = requests.put(url, json=json)
        if response.status_code != 200:
            logging.error(f"error: {response.status_code}, {response.text}")

    def update_repo_transition_setting(self,
                                       repo: str,
                                       mode: int = 1,
                                       ):
        """
        https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-transition
        :param mode: 权限管理模式. 1: 继承模式  2. 独立模式
        :param repo: 代码仓
        :return:
        """
        logging.info(f"update {repo} repo transition settings...")
        url = f"{self.base_url}/repos/{self.owner}/{repo}/transition?access_token={self.access_token}"
        json = dict(mode=mode)

        response = requests.put(url, json=json)

        if response.status_code != 200:
            logging.error(f"error: {response.status_code}, {response.text}")

    def get_org_repo(self):
        """
        获取组织所有代码仓信息
        :return:
        """
        url = f"{self.base_url}/orgs/{self.owner}/repos?access_token={self.access_token}&per_page=100"
        repos = []
        page = 1
        while True:
            _url = f"{url}&page={page}"
            response = requests.get(_url)
            [repos.append(x) for x in response.json()]

            total_page = response.headers.get("total_page")
            if not total_page or int(total_page) < page:
                break
            page += 1
            time.sleep(1.5)

        return repos

    def list_all_organization_members(self, role="all"):
        """
        https://docs.gitcode.com/docs/apis/get-api-v-5-orgs-org-members
        获取组织所有成员
        :return:
        """
        url = f"{self.base_url}/orgs/{self.owner}/members"
        page = 1
        params = {
            "role": role,
            "access_token": self.access_token,
            "page": page,
            "per_page": 100
        }
        users = []
        while True:
            response = requests.get(url, params=params)
            page += 1
            params.update(page=page)

            users.extend(response.json())

            total_page = response.headers.get("total_page", None)
            if not total_page or page > int(total_page):
                break

        return users

    def list_all_ent_members(self, role="all"):
        """
        获取企业所有成员
        :return:
        """
        url = f"{self.base_v8_url}/enterprises/{self.enterprise_id}/members"
        page = 1
        params = {
            "role": role,
            "access_token": self.access_token,
            "page": page,
            "per_page": 100
        }
        users = []
        while True:
            response = requests.get(url, params=params)
            page += 1
            params.update(page=page)

            users.extend(response.json())

            if page > int(response.headers.get("total_page")):
                break

        return users

    def update_user_role(self,
                         login_id: str,
                         role_uuid: str
                         ):
        """
        更新用户角色
        :param role_uuid: gitcode role uuid
        :param login_id: gitcode id
        :return:
        """
        url = f"{self.base_v8_url}/enterprises/{self.enterprise_id}/members/{login_id}?access_token={self.access_token}"
        params = {
            "role": "customized",
            "role_id": role_uuid
        }
        response = requests.put(url, json=params)
        if response.status_code not in [200, 201, 204]:
            logging.info(f"response status code: {response.status_code}, msg: {response.text}")

    def get_ent_issues(self, assignee: str = "none"):
        """
        https://docs.gitcode.com/docs/apis/get-api-v-5-enterprises-enterprise-issues
        获取企业所有issue
        :param assignee: issue指派人， 如果是none, 则没指派者； *为所有带有指派者的
        :return:
        """
        url = f"https://api.gitcode.com/api/v5/enterprises/{self.owner}/issues"
        page, per_page = 1, 100
        params = {
            "access_token": self.access_token,
            "state": "all",
            "page": page,
            "per_page": per_page,
            "assignee": assignee
        }
        result = []
        while True:
            params.update(page=page)
            response = requests.get(url, params=params)

            total_page = response.headers.get("total_page")
            for item in response.json():
                number = item.get("number")
                repo = item.get("repository").get("name")
                title = item.get("title")
                result.append({
                    "repo": repo,
                    "number": number,
                    "title": title
                })

            if page >= int(total_page):
                break

            page += 1

        return result

    def get_repo_issues(self, repo: str, assignee: str = None, created_after: str = None):
        """
        获取仓库下的issue
        https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-issues
        :param created_after: 返回在指定时间之后创建的问题，例如：2024-11-20T13:00:21+08:00
        :param repo:
        :param assignee: issue指派人， 如果是none, 则没指派者； *为所有带有指派者的
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/issues"
        page, per_page = 1, 100
        params = {
            "access_token": self.access_token,
            "state": "all",
            "page": page,
            "per_page": per_page,
            "assignee": assignee
        }

        if created_after:
            params.update(created_after=created_after)

        result = []
        while True:
            params.update(page=page)
            response = requests.get(url, params=params)

            total_page = response.headers.get("total_page")
            for item in response.json():
                number = item.get("number")
                # repo = item.get("repository").get("name")
                title = item.get("title")
                login = item.get("user", {}).get("login", None)
                if not login:
                    print(item.get("user"))
                    continue

                result.append({
                    "repo": repo,
                    "number": number,
                    "title": title,
                    "login": login
                })

            if page >= int(total_page):
                break

            page += 1

        return result

    def assign_issue_default_assignee(self, repo: str, number: str, title: str, assignee: str):
        """
        给issue添加默认责任人
        :param title:
        :param assignee: 默认责任人gitcode id
        :param repo:
        :param number:  issue number
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/issues/{number}?access_token={self.access_token}"
        response = requests.get(url)

        # 如果已经有责任人了，则不在更新责任人
        if response.json().get("assignee"):
            return

        # 更新责任人
        self.update_issue(number, repo, title, assignee)

    def update_issue(self, number: str, repo: str, title: str, assignee: str = None):
        """
        更新issue状态
        :param title: issue 标题
        :param repo:
        :param number:
        :param assignee: issue责任人
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/issues/{number}?access_token={self.access_token}"
        body = {
            "repo": repo,
            "title": title,
            "assignee": assignee,
        }
        response = requests.patch(url, json=body)
        if response.status_code not in [200, 201, 204]:
            logging.info(f"update issue {self.owner}/{repo}/{number} failed...")

    def create_branch_rule(self, repo: str, branch: str, rule: str):
        """
        https://docs.gitcode.com/docs/apis/put-api-v-5-repos-owner-repo-branches-setting-new
        创建保护分支规则
        :param rule: 常规分支、保护分支、只读分支
        :param repo:
        :param branch:
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/branches/setting/new?access_token={self.access_token}"
        if rule == "保护分支":
            pusher, merger = "", "admin"
        elif rule == "只读分支":
            pusher, merger = "", ""
        else:
            return

        body = {
            "wildcard": branch,
            "pusher": pusher,
            "merger": merger,
        }
        response = requests.put(url, json=body)
        if response.status_code not in [200, 201, 204]:
            logging.info(f"create repo: {repo} branchL {branch} failure...")
            logging.error(response.text)

    def create_repo(self,
                    repo: str,
                    description: str,
                    ):
        """
        创建代码仓
        :param description:
        :param repo:
        :return:
        """
        url = f"https://api.gitcode.com/api/v5/orgs/{self.owner}/repos?access_token={self.access_token}"
        body = {
            "name": repo,
            "description": description,
            "homepage": "",
            "public": 0,
            "path": repo,
            "auto_init": True,
            "default_branch": "master",
        }
        response = requests.post(url, json=body)
        if response.status_code not in [200, 201, 204]:
            logging.error(f"create repo: {repo} failure...")

    def del_org_member(self, user: str):
        """
        https://docs.gitcode.com/docs/apis/delete-api-v-5-orgs-org-memberships-username
        将用户从组织移除
        :param user:
        :return:
        """
        url = f"{self.base_url}/orgs/{self.owner}/memberships/{user}?access_token={self.access_token}"
        response = requests.delete(url)
        if response.status_code not in [200, 201, 204]:
            logging.info(f"delete user from org:{self.owner} failed...")

    def del_ent_member(self, login: str, headers):
        """
        移除企业成员
        :param headers: 请求头
        :param login: login_id
        :return:
        """
        url = f"https://web-api.gitcode.com/api/v2/enterprises/{self.enterprise_id}/enterprise-members/{login}"
        response = requests.delete(url, headers=headers)
        return response.status_code

    def get_repo_protected_branch(self, repo: str):
        """
        https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-protect-branches
        获取代码仓保护分支列表
        :param repo:
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/protect_branches?access_token={self.access_token}&per_page=100"
        response = requests.get(url)
        data = response.json()
        return data

    def update_protected_branch(self, repo: str, branch: str, merge_users: str, headers):
        """
        web-api
        更新保护分支规则， 仅支持更新合并用户权限
        :param merge_users: 拥有合并权限用户的id, 多个用户id可以用,分割；譬如 "5355243,4561812,5293307"
        :param branch: 分支名称
        :param headers: 请求头
        :param repo:
        :return:
        """
        url = f"https://web-api.gitcode.com/api/v2/projects/{self.owner}%2F{repo}/repository/branches/protect"
        body = {
            "name": branch,
            "access_level_string": {
                "push_access_levels": "",
                "merge_access_levels": ""
            },
            "push_user": "",
            "merge_user": merge_users,
            "push_role": "",
            "merge_role": "",
            "access_level": {},
            "merge_setting": {}
        }
        response = requests.put(url, headers=headers, json=body)
        if response.status_code != 200:
            logging.info(f"update repo:{repo} branch: {branch} protected attr failed")

    def get_repo_member(self, repo: str):
        """
        https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-collaborators
        获取仓库成员
        :param repo:
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/collaborators?access_token={self.access_token}"
        page = 1
        users = []
        params = dict(page=page, per_page=100)
        while True:
            response = requests.get(url, params=params)
            page += 1
            params.update(page=page)
            if response.status_code in [200, 201, 204]:
                users.extend(response.json())

            total_page = response.headers.get("total_page")
            if not total_page or page > int(total_page):
                break

        return users

    def rm_repo_members(self, repo: str, login: str):
        """
        https://docs.gitcode.com/docs/apis/delete-api-v-5-repos-owner-repo-collaborators-username
        删除仓库成员
        :param repo:
        :param login:
        :return:
        """
        url = f"{self.base_url}/repos/{self.owner}/{repo}/collaborators/{login}?access_token={self.access_token}"
        response = requests.delete(url)
        if response.status_code not in [200, 201, 204]:
            logging.info(f"delete {login} from repo {repo} fail...")
