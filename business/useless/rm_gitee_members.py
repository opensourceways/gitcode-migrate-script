
"""
清理gitee企业成员
"""

from base.gitee_app import GiteeApp


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 enterprise: str
                 ):
        self.gitee_app = GiteeApp(access_token=access_token,
                                  owner=owner,
                                  enterprise=enterprise
                                  )

    def run(self):
        with open("../data/gitee_users.txt", "r") as f:
            users = f.readlines()

        for user in users:
            user = user.strip(" ").strip("\n")
            if user:
                self.gitee_app.clear_enterprise_user(user)


if __name__ == '__main__':
    app = App(access_token="",
              owner="ascend",
              enterprise="HUAWEI-ASCEND"
              )
    app.run()
