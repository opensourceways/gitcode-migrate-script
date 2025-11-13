from base.gitcode_app import GitcodeApp

from config import AscendDev, GitcodeAccessToken

"""
Gitcode: 更新社区开发者角色  （开发者 -->  Ascend开发者/生态开发者）
"""


def main():
    gitcode_app = GitcodeApp(access_token=GitcodeAccessToken,
                             owner="ascend"
                             )
    users = gitcode_app.list_all_ent_members(role="developer")

    for user in users:
        role = user.get("role")

        if role in ["admin", "maintainer"]:
            continue

        login = user.get("user").get("login")
        gitcode_app.update_user_role(login, AscendDev)


if __name__ == '__main__':
    main()
