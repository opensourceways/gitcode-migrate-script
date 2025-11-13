import logging

from base.gitee_app import GiteeApp
from config import GiteeV5Token

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

"""
同步完issue后检查两个平台的issue是否一致
"""


class LockGiteeRepos:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 ):
        self.gitee_app = GiteeApp(access_token, owner, enterprise)

    def run(self):
        # repos = self.gitee_app.get_repos()

        repos = [
            "owners_collections",
        ]

        for repo in repos:
            # self.gitee_app.update_readme(repo)  # 这个在最后同步完再执行 !!!
            self.gitee_app.update_readme_sh(repo)  # 这个在最后同步完再执行 !!!
            self.gitee_app.new_file_tips(repo)  # 这个在最后同步完再执行 !!!

            self.gitee_app.update_repo_settings(repo)
            self.gitee_app.lock_repo(repo)


if __name__ == '__main__':
    app = LockGiteeRepos(access_token=GiteeV5Token,
                         owner="ascend",
                         enterprise="HUAWEI-ASCEND",
                         )
    app.run()
