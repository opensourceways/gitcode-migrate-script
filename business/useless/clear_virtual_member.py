import logging
import time

from base.gitcode_app import GitcodeApp
from config import GitCodeRequestHeaders, GitcodeAccessToken

"""
将不存在的用户从组织和企业中清除出去
"""


class App:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def clear_ent_members(self):
        """
        清除企业用户
        :return:
        """
        users = self.gitcode_app.list_all_ent_members()
        usernames = [x.get("user").get("login") for x in users]

        for name in usernames:
            if not self.gitcode_app.check_user_exist(name):
                logging.info(f"delete virtual enterprise user: {name}")
                self.gitcode_app.del_ent_member(name, GitCodeRequestHeaders)
                time.sleep(1.5)

    def clear_org_member(self):
        """
        清除组织用户
        :return:
        """
        users = self.gitcode_app.list_all_organization_members()
        usernames = [x.get("login") for x in users]

        for username in usernames:
            if not self.gitcode_app.check_user_exist(username):
                logging.info(f"delete virtual enterprise user: {username}")
                self.gitcode_app.del_org_member(username)
                time.sleep(1.5)

    def run(self):
        self.clear_ent_members()
        self.clear_org_member()


if __name__ == '__main__':
    app = App(access_token=GitcodeAccessToken,
              owner="cann",
              )
    app.run()
