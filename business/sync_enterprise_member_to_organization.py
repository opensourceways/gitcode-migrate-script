"""
定期将企业成员同步至组织; 将组织、仓库成员同步至企业
"""
import logging
import time

from base.gitcode_app import GitcodeApp
from config import AscendDev, CannDEV, BoostKitDEV, AscendMirrorDev, GitcodeAccessToken


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        if self.owner.lower() == "ascend":
            self.role_dev = AscendDev
        elif self.owner.lower() == "cann":
            self.role_dev = CannDEV
        elif self.owner.lower() == "boostkit":
            self.role_dev = BoostKitDEV
        else:
            self.role_dev = AscendMirrorDev

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def sync_ent_to_org(self):
        """
        将企业用户同步至组织
        :return:
        """
        logging.info("start sync member to org...")
        enterprise_member = self.gitcode_app.list_all_ent_members()
        organization_member = self.gitcode_app.list_all_organization_members()

        enterprise_member = {x.get("user").get("login"): x for x in enterprise_member}
        organization_member = [x.get("login") for x in organization_member]

        for name, item in enterprise_member.items():
            if name not in organization_member and self.gitcode_app.check_user_exist(name):
                logging.info(f"sync enterprise user: {name} to org...")
                self.gitcode_app.invite_to_organization(name, item.get("role"), item.get("role_id"))
                time.sleep(1.5)

    def sync_org_to_ent(self):
        """
        将组织用户同步至企业
        :return:
        """
        logging.info("start sync org member to ent...")
        org_usernames = [x.get("login") for x in self.gitcode_app.list_all_organization_members()]
        ent_mem = [x.get("user").get("login") for x in self.gitcode_app.list_all_ent_members()]

        for user in org_usernames:
            if user not in ent_mem and self.gitcode_app.check_user_exist(user):
                logging.info(f"invite org {user} to ent...")
                self.gitcode_app.invite_to_enterprise(user, self.role_dev)
                time.sleep(1.5)

    def sync_repo_to_ent(self):
        """
        将代码仓成员同步至企业
        :return:
        """
        logging.info("start sync repo member to ent...")
        repos = [x.get("name") for x in self.gitcode_app.get_org_repo()]
        ent_mem = [x.get("user").get("login") for x in self.gitcode_app.list_all_ent_members()]

        for repo in repos:
            logging.info(f"start deal with: {repo}")
            members = [x.get("login") for x in self.gitcode_app.get_repo_member(repo)]
            for member in members:
                if member not in ent_mem and self.gitcode_app.check_user_exist(member):
                    logging.info(f"invite {member} to ent...")
                    self.gitcode_app.invite_to_enterprise(member, self.role_dev)
                    ent_mem.append(member)
                    time.sleep(1.5)

    def run(self):
        while True:
            logging.info(f"start run {self.owner}...")
            try:
                self.sync_ent_to_org()  # 将企业成员同步至组织
                self.sync_org_to_ent()  # 将组织成员同步至企业
                self.sync_repo_to_ent()  # 将仓库成员同步至企业
            except Exception as err:
                logging.error(err)
            logging.info("sync finished...")
            time.sleep(5 * 60)


if __name__ == '__main__':
    app = App(
        access_token=GitcodeAccessToken,
        owner="cann",
    )
    app.run()
