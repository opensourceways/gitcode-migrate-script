"""
定期将企业成员同步至预迁移组织
"""

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken
from config import AscendMirrorDev


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 dis_owner: str,
                 role_id: str
                 ):
        """
        :param access_token:
        :param owner: 源迁移组织
        :param dis_owner: 目标迁移组织
        :param role_id: 目标迁移组织的用户角色id
        """
        self.access_token = access_token
        self.owner = owner
        self.dis_owner = dis_owner
        self.role_id = role_id

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)
        self.dis_gitcode_app = GitcodeApp(access_token=access_token, owner=dis_owner)

    def run(self):
        origin_members = self.gitcode_app.list_all_ent_members()
        dis_members = self.dis_gitcode_app.list_all_ent_members()

        origin_members = {x.get("user").get("name"): x for x in origin_members}
        dis_members = {x.get("user").get("name"): x for x in dis_members}

        for name, item in origin_members.items():
            if name not in dis_members:
                self.dis_gitcode_app.invite_to_enterprise(name, self.role_id)


if __name__ == '__main__':
    app = App(access_token=GitcodeAccessToken,
              owner="ascend",
              dis_owner="ascend-mirror",
              role_id=AscendMirrorDev
              )
    app.run()
