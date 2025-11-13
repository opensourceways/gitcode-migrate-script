import logging

from base.gitee_app import GiteeApp
from base.gitcode_app import GitcodeApp

from config import GitcodeAccessToken, GiteeV5Token

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

"""
获取gitee平台 组织下所有代码仓
"""


class GetOwnerRepos:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 ):
        self.gitee_app = GiteeApp(access_token, owner, enterprise)

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run(self):
        repos = self.gitee_app.get_repos()
        # repos = [x.get("name") for x in self.gitcode_app.get_org_repo()]

        with open("../data/repos.txt", "w+") as f:
            for line in repos:
                f.writelines(line + "\n")


if __name__ == '__main__':
    app = GetOwnerRepos(
        access_token=GiteeV5Token,
        # access_token="724dce40cd8fe74cc6d1d4c2b340b9d9",
        owner="ascend",
        enterprise="cann",
    )
    app.run()
