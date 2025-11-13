"""
邀请成员至代码仓
"""
import json
import logging

from base.gitcode_app import GitcodeApp
from config import CannDEV, AscendDev, GitcodeAccessToken


class App:
    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner
        self.dev_role = AscendDev if owner == "ascend" else CannDEV
        self.dev_name = "Ascend开发者" if owner == "ascend" else "生态开发者"

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run2(self):
        repo = "ops-nn-dev"
        members = self.gitcode_app.get_repo_member(repo)
        for member in members:
            name = member.get("name")
            role = member.get("role_name_cn")
            if role == "管理员":
                continue
            logging.info(f"invite user: {name} to repo as {role}")
            self.gitcode_app.invite_to_repo(name, "ops-nn", role)

    def run3(self):
        with open("../data/gitcode_repo_members.json", "r+") as f:
            data = json.load(f)

        for repo, members in data.items():
            for member in members:
                self.gitcode_app.invite_to_repo(member, repo, "BoostKit开发者")

    def run(self):
        # repos = [x.get("name") for x in self.gitcode_app.get_org_repo()]
        # repos = [x for x in repos if "ops" in x]
        # repos.append("opbase")

        repos = [
            "MindIE-LLM",
            "MindIE-Motor",
            "MindIE-SD",
            "MindIE-Turbo",
            # "ascend-faster-transformer",
            # "mstt",
            # "msit"
            # "openeuler-agreements"
        ]
        users = [
            "hely123",
        ]
        for user in users:
            self.gitcode_app.invite_to_enterprise(user, self.dev_role)
            self.gitcode_app.invite_to_organization(user, self.dev_name, self.dev_role)
            # self.gitcode_app.invite_to_organization(user, "admin")

            for repo in repos:
                logging.info(f"invite user:{user} to repo: {repo}...")
                self.gitcode_app.invite_to_repo(user, repo, self.dev_name)
                # self.gitcode_app.invite_to_repo(user, repo, "BoostKit开发者")


if __name__ == '__main__':
    app = App(access_token=GitcodeAccessToken,
              owner="ascend",
              )
    app.run()
