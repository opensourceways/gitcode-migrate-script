import json
import yaml

from base.gitee_app import GiteeApp


class App:

    def __init__(self,
                 owner: str,
                 enterprise: str,
                 access_token: str,
                 v8_token: str
                 ):
        """
        :param owner:
        :param enterprise
        :param access_token:
        :param v8_token:
        """
        self.owner = owner
        self.enterprise = enterprise
        self.access_token = access_token
        self.v8_token = v8_token

        self.gitee_app = GiteeApp(access_token=access_token,
                                  owner=owner,
                                  enterprise=enterprise
                                  )

    def run(self):
        with open("../data/sig.yaml", "r") as f:
            sig_info = yaml.safe_load(f)

        # ent_members = self.gitee_app.get_enterprise_members(self.v8_token)

        # 保存至本地，避免每次都请求
        ent_member_path = f"../data/{self.owner}_ent_member.json"
        # with open(ent_member_path, "w") as f:
        #     json.dump(ent_members, f, indent=4)

        with open(ent_member_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        repos = ["ascend-deployer", "ascend-docker-image", "mindsdk-referenceapps", "mindxdl-deploy", "RecSDK", "mind-cluster", "rec-sdk-next"]
        repo_members = []
        for repo in repos:
            repo_members.extend(self.gitee_app.get_repo_members(repo))

        all_info = []
        for item in repo_members:
            _tmp = []
            repo = item.get("repo")
            login_id = item.get("login_id")
            _name = item.get("name", "")

            _tmp.extend([repo, f"{login_id}"])

            ent_item = data.get(login_id, None)
            if ent_item:
                username = ent_item.get("username") or ""
                remark = ent_item.get("remark") or ""
                email = ent_item.get("email") or ""
                phone = ent_item.get("phone") or ""
                _tmp.extend([username, remark, email, phone])
            else:
                _tmp.extend(["", "", "", ""])

            sig = sig_info.get(repo, {})

            if login_id in sig.get("branch_keeper", []):
                _tmp.append("branch_keeper")
            elif login_id in sig.get("approvers", []):
                _tmp.append("approvers")
            elif login_id in sig.get("reviewers", []):
                _tmp.append("reviewers")

            all_info.append(_tmp)

        repo_member_path = f"../data/{self.owner}_repo_member.txt"
        with open(repo_member_path, "w", encoding="utf-8") as f:
            for line in all_info:
                f.write(";".join(line) + "\n")


if __name__ == '__main__':
    app = App(
        owner="ascend",
        enterprise="HUAWEI-ASCEND",
        access_token="",
        v8_token=""
    )
    app.run()
