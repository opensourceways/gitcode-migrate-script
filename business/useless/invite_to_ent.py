"""
邀请成员至代码仓
"""

from base.gitcode_app import GitcodeApp
from config import BoostKitDEV, GitcodeAccessToken, AscendDev


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run(self):
        users = [
            "whjnbm",
        ]
        for user in users:
            self.gitcode_app.invite_to_enterprise(user, "dd402f032d764b83ab4475fe6b316209")


if __name__ == '__main__':
    app = App(access_token=GitcodeAccessToken,
              owner="openeuler-test",
              )
    app.run()
