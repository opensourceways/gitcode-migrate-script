"""
openGauss 指定默认责任人， 刷新历史数据
"""
import logging

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

DefaultAssignee = "TestManager"


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run(self):

        # repos = self.gitcode_app.get_org_repo()
        # repos = [x.get("name") for x in repos]
        #
        # for repo in repos:
        #     if repo in ["gitcode"]:
        #         continue
        #
        #     logging.info(f"Get repo: {repo} issues...")
        #     issues = self.gitcode_app.get_repo_issues(repo)
        #
        #     for issue in issues:
        #         self.gitcode_app.assign_issue_default_assignee(assignee=DefaultAssignee, **issue)

        issues = self.gitcode_app.get_ent_issues()
        for issue in issues:
            repo = issue.get("repo")
            if repo in ["infra", "gitcode", "og-agreements"]:
                continue
            logging.info(f"deal issue: {issue}")
            self.gitcode_app.assign_issue_default_assignee(assignee=DefaultAssignee, **issue)


if __name__ == '__main__':
    app = App(access_token=GitcodeAccessToken,
              owner="opengauss",
              )
    app.run()
