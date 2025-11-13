import json
import time

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

"""
读取gitcode Webhooks
"""


class GetGitcodeWebhooks:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.gitcode_app = GitcodeApp(access_token, owner)

    @staticmethod
    def write_down(data: dict):
        with open(r"../data/webhooks.json", "w") as f:
            _f = json.dumps(data)
            f.write(_f)

    @staticmethod
    def load_json():
        with open(r"../data/webhooks.json", "r") as f:
            return json.load(f)

    def run(self):
        # 需要获取webhooks的代码仓
        # repos = [
        #     "torchair",
        # ]
        #
        # result = {}
        # # 将代码仓的webhook获取后保存至result
        # for repo in repos:
        #     webhooks = self.gitcode_app.get_repo_webhooks(repo)
        #     result[repo] = webhooks
        #
        # self.write_down(data=result)
        result = self.load_json()

        # 将获取的webhook重新保存至新代码仓
        for repo, webhooks in result.items():
            for webhook in webhooks:
                # repo = repo.rstrip("-bk")
                self.gitcode_app.add_repo_webhook(repo, **webhook)
                time.sleep(1.5)


if __name__ == '__main__':
    app = GetGitcodeWebhooks(owner="ascend",
                             access_token=GitcodeAccessToken
                             )
    app.run()
