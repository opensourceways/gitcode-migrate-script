import time

from base.gitcode_app import GitcodeApp
from base.gitee_app import GiteeApp

from config import GitcodeAccessToken, GiteeV5Token

"""
同步项目描述和默认分支
"""


class App:

    def __init__(self,
                 gitee_owner: str,
                 gitcode_owner: str,
                 gitee_token: str,
                 gitcode_token: str,
                 ):
        self.gitee_owner = gitee_owner
        self.gitcode_owner = gitcode_owner
        self.gitee_token = gitee_token
        self.gitcode_token = gitcode_token

        self.gitcode_app = GitcodeApp(access_token=gitcode_token, owner=gitcode_owner)
        self.gitee_app = GiteeApp(access_token=gitee_token, owner=gitee_owner, enterprise=gitee_owner)

    def run(self):
        gitcode_repos = self.gitcode_app.get_org_repo()

        # _repos = [
        #     "ascgen-dev",
        #     "cann-graph-engine-dev",
        #     "metadef",
        #     "ACLLite",
        #     "ascend-attention",
        #     "cann_b",
        #     "cann_h",
        #     "cann_k",
        #     "cann_m",
        #     "cann_z",
        #     "cann-autofuse",
        #     "cann-hccl-tsingmao",
        #     "cann-h-sci",
        #     "cann-recipes",
        #     "comm-algo",
        #     "hccl_cust",
        #     "ops_ascendc",
        #     "PyDFlow",
        #     "tensorflow",
        #     "modelzoo",
        #     "ModelZoo-PyTorch",
        #     "modelzoo-GPL"
        # ]

        for item in gitcode_repos:
            name = item.get("name")
            if name in ["sync_repos", "community", "sync-repos-boostkit"]:
                continue

            description = item.get("description")
            default_branch = item.get("default_branch")

            data = self.gitee_app.get_repo_info(name)

            _description = data.get("description")
            _default_branch = data.get("default_branch")

            params = dict(description=None, default_branch=_default_branch)
            if not description and _description:
                params.update(description=_description)

            self.gitcode_app.update_repo_attr(repo=name, **params)
            time.sleep(1.5)


if __name__ == '__main__':
    app = App(
        gitee_owner="ascend",
        gitcode_owner="mirror-test",
        gitee_token=GiteeV5Token,
        gitcode_token=GitcodeAccessToken,
    )
    app.run()
