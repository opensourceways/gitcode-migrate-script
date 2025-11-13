import logging
import time

from base.gitcode_app import GitcodeApp

from config import GitCodeRequestHeaders, GitcodeAccessToken

"""
修改分支属性
"""


class UpdateGitcodeBranchAttr:

    def __init__(self, access_token, owner):
        self.access_token = access_token
        self.owner = owner

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run(self):
        repos = [
            "torchair"
        ]
        merge_users = "5355243"  # 需要结合项目本身自定义
        for repo in repos:
            items = self.gitcode_app.get_repo_protected_branch(repo)
            for item in items:
                branch = item.get("name")
                logging.info(f"update {repo}/{branch} protected attr")
                self.gitcode_app.update_protected_branch(repo, branch, merge_users, GitCodeRequestHeaders)
                time.sleep(1.5)


if __name__ == '__main__':
    app = UpdateGitcodeBranchAttr(
        access_token=GitcodeAccessToken,
        owner="ascend",
    )
    app.run()
