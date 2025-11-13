import os
from ruamel.yaml import YAML

from base.gitcode_app import GitcodeApp
from config import GitcodeAccessToken

"""
将代码仓数据转换成sig repo.yaml
"""


def main():
    app = GitcodeApp(access_token=GitcodeAccessToken, owner="BoostKit")
    repos = app.get_org_repo()
    for repo in repos:
        name = repo.get("name")
        data = {
            "name": name,
            "type": "public" if repo.get("public") else "private",
            "description": repo.get("description"),
            "branches": [{
                "name": "master",
                "type": ""
            }]
        }
        first = name[0].lower()
        path = f"../data/sig/{first}"

        os.makedirs(path, exist_ok=True)

        yaml = YAML()
        file = f"{path}/{name}.yaml"
        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(data, f)


if __name__ == '__main__':
    main()
