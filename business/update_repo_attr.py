import json
import time

from base.gitcode_app import GitcodeApp

from config import GitcodeAccessToken


class UpdateRepoAttr:

    def __init__(self,
                 owner: str,
                 access_token: str
                 ):
        self.owner = owner
        self.access_token = access_token
        self.gitcode_app = GitcodeApp(owner=owner, access_token=access_token)

    @classmethod
    def save_user(cls, data):
        with open("../data/gitcode_repo_members.json", "w+") as f:
            _j = json.dumps(data)
            f.write(_j)

    @classmethod
    def load_user(cls):
        with open("../data/gitcode_repo_members.json", "r+") as f:
            return json.load(f)

    def run(self):
        repos = self.gitcode_app.get_org_repo()

        for repo in repos:
            name = repo.get("name")
            _private = repo.get("private")

            # 1. 仓库设置
            self.gitcode_app.update_repo_setting(name)
            # 2. PR 设置
            self.gitcode_app.update_pr_settings(name, merged_commit_author="created_by")
            time.sleep(2)
            # 3. 设置成独立模式
            self.gitcode_app.update_repo_transition_setting(name, mode=2)


if __name__ == '__main__':
    app = UpdateRepoAttr(
        owner="mirror-test",
        access_token=GitcodeAccessToken
    )
    app.run()
