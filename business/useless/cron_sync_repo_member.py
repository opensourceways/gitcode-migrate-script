import json
import logging
import time

import requests

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken, GitcodeClientID, GitcodeHeaderCookie

"""
将原在代码仓成员且使用Gitee授权登录的用户，邀请至相应代码仓
"""


class App:
    def __init__(self,
                 owner: str,
                 access_token: str
                 ):
        self.owner = owner
        self.gitcode_app = GitcodeApp(access_token, owner)
        self.user_info = self.load_user_info()
        # self.user_map = {x: "" for x in self.user_info.keys()}
        self.users = self.load_user()

    @classmethod
    def load_user_info(cls) -> dict:
        """
        gitee id与其加入的仓库信息
        :return:
        """
        with open("../../data/repo_member.json", "r+") as f:
            return json.load(f)

    @classmethod
    def save_user(cls, users: list[str]):
        with open("../../data/already_in_users.txt", "w", encoding="utf-8") as f:
            for user in users:
                f.write(f"{user}\n")

    @classmethod
    def load_user(cls):
        with open("../../data/already_in_users.txt", "r", encoding="utf-8") as f:
            data = f.readlines()
            return [x.strip("\n") for x in data]

    @staticmethod
    def get_by_gitee_id(gitee_id: str) -> str:
        """
        通过gitee id 获取gitcode id
        :param gitee_id:
        :return:
        """
        url = f'https://api.gitcode.com/api/v5/user/{gitee_id}/gitcode/user'
        params = dict(client_id=GitcodeClientID)
        headers = dict(Cookie=GitcodeHeaderCookie)

        response = requests.get(url, params=params, headers=headers)
        return response.json().get("username")

    def run(self):
        while True:
            logging.info(f"start run {self.owner}...")
            for user, repos in self.user_info.items():

                if user not in self.users:
                    gitcode_user = self.get_by_gitee_id(user)
                    if gitcode_user and self.gitcode_app.check_user_exist(gitcode_user):
                        self.users.append(user)
                        for repo in repos:
                            logging.info(f"add user: {gitcode_user} to repo： {repo}")
                            self.gitcode_app.invite_to_repo(gitcode_user, repo, "Ascend开发者")
                            time.sleep(1)

            self.save_user(self.users)


if __name__ == '__main__':
    app = App(owner="ascend",
              access_token=GitcodeAccessToken
              )
    # app.run()
    app.get_by_gitee_id("carolinayuan")