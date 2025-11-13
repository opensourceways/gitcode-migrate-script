import time

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

"""
Gitcode: 将gitcode平台的代码仓改为私有/公开代码仓， 并打开 合并请求PR预合并 | 允许合并请求合并后继续做代码检视和评论 开关
"""


class UpdateGitcodeRepoPrivate:

    def __init__(self,
                 owner: str,
                 access_token: str
                 ):
        self.gitcode_app = GitcodeApp(access_token, owner)

    def run(self):
        repos = [x.get("name") for x in self.gitcode_app.get_org_repo()]
        # repos= [
        #     "mstt",
        #     "msit",
        #     "DrivingSDK",
        #     "openmind",
        #     "openmind-hub",
        #     "apex",
        #     "apex-develop",
        #     "MindSpeed",
        #     "MindSpeed-LLM",
        #     "MindSpeed-MM",
        #     "MindSpeed-RL",
        #     "pytorch",
        #     "Tensorpipe",
        #     "op-plugin",
        #     "vision",
        #     "joint-innovation-rl"
        # ]

        for repo in repos:
            # self.gitcode_app.update_repo_attr(repo,
            #                                   private=False,  # 将代码仓设置成公仓
            #                                   default_branch="master",  # 设置默认分支
            #                                   )

            self.gitcode_app.update_pr_settings(repo,
                                                add_notes_after_merged=True,  # 允许合并请求合并后继续做代码检视和评论
                                                )

            self.gitcode_app.update_repo_setting(repo,
                                                 generate_pre_merge_ref=True,  # 合并请求PR预合并
                                                 )

            time.sleep(1.5)  # 应付限流


if __name__ == '__main__':
    app = UpdateGitcodeRepoPrivate(owner="boostkit",
                                   access_token=GitcodeAccessToken
                                   )
    app.run()
