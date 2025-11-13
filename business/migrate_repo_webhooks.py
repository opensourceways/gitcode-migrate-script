import logging
import openpyxl

from base.gitee_app import GiteeApp
from base.gitcode_app import GitcodeApp

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")

"""
将gitee代码仓webhook同步至gitcode
"""


class MigrateRepoWebhook:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str,
                 gitcode_access_token: str,
                 gitcode_owner: str,
                 ):
        self.gitee_app = GiteeApp(access_token, owner, enterprise)
        self.gitcode_app = GitcodeApp(gitcode_access_token, gitcode_owner)

    @staticmethod
    def write_down(data: list[list]):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = "webhooks"
        for row, line in enumerate(data):
            for column, ele in enumerate(line):
                sheet.cell(row=row + 1, column=column + 1, value=ele)
        wb.save(f"../data/代码仓webhook.xlsx")

    def get_webhooks(self):
        repos = self.gitee_app.get_repos()
        webhooks = []
        for repo in repos:
            _tmp = self.gitee_app.get_repo_webhook(repo)
            webhooks.extend(webhooks)

        return webhooks

    def run(self):
        # step1: 从gitee读取代码仓webhooks, 并写入excel文件
        webhooks = self.get_webhooks()
        self.write_down(webhooks)

        # step2: 将webhook数据写入gitcode
        for webhook in webhooks:
            self.gitcode_app.add_repo_webhook(**webhook)


if __name__ == '__main__':
    app = MigrateRepoWebhook(
        access_token="",
        owner="",
        enterprise="",
        gitcode_access_token="",
        gitcode_owner=""
    )
    app.run()
