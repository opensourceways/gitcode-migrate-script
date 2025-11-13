import logging

from base.gitee_app import GiteeApp

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

"""
同步完issue后检查两个平台的issue是否一致
"""


class CheckIssueIsLack:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 ):
        self.gitee_app = GiteeApp(access_token, owner, enterprise)

    @staticmethod
    def write_down(issues):
        path = "../data/GiteeIssues.txt"
        with open(path, "a+", encoding="utf-8") as f:
            for issue in issues:
                item = ",".join(issue) + "\n"
                f.writelines(item)

    def run(self):
        repos = self.gitee_app.get_repos()
        repos = [x.split("/")[1] for x in repos]  # 需要结合项目进行代码仓过滤

        for repo in repos:
            logging.info(f"start deal with repo: {repo}...")
            issues = self.gitee_app.get_repo_issue(repo)
            self.write_down(issues)


if __name__ == '__main__':
    app = CheckIssueIsLack(access_token="",
                           owner="",
                           enterprise="",
                           )
    app.run()
