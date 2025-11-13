"""
获取代码仓成员信息并写入csv
"""
import logging

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken


class SyncRepoMemberToEntApp:

    def __init__(self,
                 access_token: str,
                 owner: str,
                 ):
        self.access_token = access_token
        self.owner = owner

        self.gitcode_app = GitcodeApp(access_token=access_token, owner=owner)

    def run(self):
        repos = [x.get("name") for x in self.gitcode_app.get_org_repo()]

        result = []
        for repo in repos:
            logging.info(f"start deal with: {repo}")
            members = self.gitcode_app.get_repo_member(repo)
            for member in members:
                if member.get("permission") == "admin":
                    continue
                name = member.get("name")
                email = member.get("email")
                line = f"{repo},{name},{email}\n"
                result.append(line)

        with open("../data/repo_members.csv", "w", encoding="utf-8") as f:
            f.writelines(result)


if __name__ == '__main__':
    app = SyncRepoMemberToEntApp(
        access_token=GitcodeAccessToken,
        owner="cann",
    )
    app.run()
