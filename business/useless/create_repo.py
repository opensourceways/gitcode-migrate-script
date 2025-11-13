import yaml

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

"""
Gitcode: 新建代码仓
"""


def main():
    gitcode_app = GitcodeApp(access_token=GitcodeAccessToken,
                             owner="BoostKit"
                             )
    with open("../data/a.yaml", encoding="utf-8") as f:
        repo_info = yaml.safe_load(f)

    for repo in repo_info:
        name = repo.get("name")
        description = repo.get("description")
        gitcode_app.create_repo(repo=name, description=description)


if __name__ == '__main__':
    main()
