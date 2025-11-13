import json

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

"""
获取gitcode代码仓成员
"""


class App:
    def __init__(self,
                 owner: str,
                 access_token: str
                 ):
        self.owner = owner
        self.gitcode_app = GitcodeApp(access_token, owner)

    @classmethod
    def save_user(cls, data):
        with open("../data/gitcode_repo_members.json", "w+") as f:
            _j = json.dumps(data)
            f.write(_j)

    @classmethod
    def load_user(cls):
        with open("../data/gitcode_repo_members.json", "r+") as f:
            return json.load(f)

    def run(self):
        repos = [
            "catlass",
            "Mind-KernelInfra",
            "ascend-transformer-boost",

            # "MindSpeed-Core-MS",
        ]

        result = self.load_user() or {}
        for repo in repos:
            users = self.gitcode_app.get_repo_member(repo)
            result[repo] = [x.get("login") for x in users]

        self.save_user(result)


if __name__ == '__main__':
    app = App(owner="cann",
              access_token=GitcodeAccessToken
              )
    app.run()
