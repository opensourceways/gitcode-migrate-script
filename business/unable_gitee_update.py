import time
import logging
import requests
import subprocess

from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

X_Csrf_Token = ""
Cookie = ""
AccountPwd = "ascend-ci-bot:****"


class App:
    def __init__(self,
                 owner: str,
                 gitcode_token: str,
                 gitcode_pwd: str
                 ):
        self.owner = owner
        self.gitcode_token = gitcode_token
        self.gitcode_pwd = gitcode_pwd

        self.repos = [
            "ascend/modelzoo",
            "ascend/ModelZoo-PyTorch",
            "ascend/modelzoo-GPL",
            "ascgen-dev",
            "cann-graph-engine-dev",
            "metadef",
            "ACLLite",
            "cann_m",
            "cann_z",
            "PyDFlow",
            "tensorflow"
        ]

    def update_code(self, repo):
        """
        更新代码
        """
        gitee_url = f"https://{AccountPwd}@gitee.com/{self.owner}/{repo}.git"
        gitcode_url = f"git@gitcode.com:mirror-test/{repo}.git"
        subprocess.call(["../tools/update_repo_code.sh", gitee_url, gitcode_url, repo])

    def update_repo_settings(self, repo: str):
        """
        禁用在线编辑、提交pr、新增issue
        :param repo:
        :return:
        """
        owner, repo = repo.split("/")
        url = f"https://gitee.com/{owner}/{repo}"
        payload = {
            "online_edit_enabled": 1,
            "project[readonly_issue]": 0,
            "project[readonly_pull_request]": 0,
        }
        headers = {
            "X-Csrf-Token": X_Csrf_Token,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": Cookie
        }
        response = requests.put(url, data=payload, headers=headers)
        if response.status_code not in [200, 201, 204]:
            logging.error(f"lock repo {repo} fail, {response.text}")
        logging.info(f"lock repo: {repo} suc...")

    def gitee_setting(self):
        for repo in self.repos:
            logging.info(f"set repo: {repo}...")
            self.update_repo_settings(repo)
            self.update_code(repo)
            time.sleep(3)

    def rename_repo(self):
        """
        给代码仓重命名
        :return:
        """
        for repo in self.repos:
            url = f"https://api.gitcode.com/api/v5/repos/{self.owner}/{repo}?access_token={self.gitcode_token}"
            body = dict(name=f"{repo}-bk", path=f"{repo}-bk")
            response = requests.patch(url, json=body)
            if response.status_code not in [200, 201, 204]:
                logging.error("modify repo name failed...")
            logging.info(f"rename repo: {repo} suc...")

    def migrate_repo(self):
        """
        转移仓库
        :return:
        """
        for repo in self.repos:
            repo = f"{repo}-bk"
            url = f"https://api.gitcode.com/api/v5/org/boostkit/projects/{repo}/transfer?access_token={self.gitcode_token}"
            body = dict(transfer_to="mirror-test", password=self.gitcode_pwd)
            response = requests.post(url, json=body)
            if response.status_code not in [200, 201, 204]:
                logging.error("modify repo name failed...")
            logging.info(f"migrate repo: {repo} suc...")

    def run(self):
        while True:
            hour = datetime.today().hour
            if hour == 15:
                self.gitee_setting()
                #
                # time.sleep(5)
                #
                # self.rename_repo()
                #
                # time.sleep(5)

                # self.migrate_repo()

                break

            logging.info("sleep for 5 minus...")
            time.sleep(5 * 60)


if __name__ == '__main__':
    app = App(owner="ascend",
              gitcode_token="-****",
              gitcode_pwd="***!"
              )
    app.run()
