import logging
import json

from base.gitee_app import GiteeApp
from config import GiteeV5Token

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

"""
获取gitee 私仓的仓库成员
"""


class GetReposMembers:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 ):
        self.gitee_app = GiteeApp(access_token, owner, enterprise)

    @staticmethod
    def clear_history_data():
        """
        清理历史数据
        :return:
        """
        with open(r"../data/repo_member.json", "r+") as f:
            data = json.load(f)

        with open("../data/already_in_users.txt", "r+") as f:
            users = [x.strip("\n") for x in f.readlines()]

        for user in users:
            data.pop(user, None)

        with open(r"../data/repo_member.json", "w+") as f:
            _f = json.dumps(data)
            f.write(_f)

        with open("../data/already_in_users.txt", "w+") as f:
            f.write("")

    def run(self):
        repos = [
            "joint-innovation-rl",
        ]

        users = []
        for repo in repos:
            users.extend(self.gitee_app.get_repo_members(repo))

        with open(r"../data/repo_member.json", "r+") as f:
            user_map = json.load(f) or {}

        for user in users:
            repo = user.get("repo")
            login_id = user.get("login_id")
            user_map.setdefault(login_id, []).append(repo)

        with open(r"../data/repo_member.json", "w+") as f:
            _f = json.dumps(user_map)
            f.write(_f)


if __name__ == '__main__':
    app = GetReposMembers(access_token=GiteeV5Token,
                          owner="ascend",
                          enterprise="ascend",
                          )
    app.run()
    # app.clear_history_data()
