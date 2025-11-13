"""
同步 Gitee分支属性
"""
import logging
import time

from base.gitee_app import GiteeApp
from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken, GiteeV5Token, GiteeV8Token


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 v8_token: str,
                 gitcode_token: str,
                 gitcode_owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner
        self.enterprise = enterprise
        self.v8_token = v8_token
        self.gitcode_token = gitcode_token

        self.gitee_app = GiteeApp(access_token=access_token, owner=owner, enterprise=enterprise)
        self.gitcode_app = GitcodeApp(access_token=gitcode_token, owner=gitcode_owner)

    def run(self):
        repos = [
            "torchair",
        ]

        result = {}
        for repo in repos:
            branches = self.gitee_app.get_repo_branches_attr(repo, self.v8_token)
            result.update({
                repo: branches
            })

        for repo, branches in result.items():
            for branch in branches:
                branch_name = branch.get("name")
                branch_attr = branch.get("branch_type").get("name")
                logging.info(f"sync repo: {repo}| branch: {branch} rule...")
                self.gitcode_app.create_branch_rule(repo, branch_name, branch_attr)
                time.sleep(1.5)


if __name__ == '__main__':
    app = App(access_token=GiteeV5Token,
              owner="ascend",
              gitcode_owner="ascend",
              enterprise="HUAWEI-ASCEND",
              v8_token=GiteeV8Token,
              gitcode_token=GitcodeAccessToken
              )
    app.run()

