import requests


def func():
    owner = "cann"
    repo = "ops-nn"

    params = dict(
        access_token="**",
        pt="2025-10-01",
        # action_names="git_download",
    )

    url = f"https://api.gitcode.com/api/v5/repos/{owner}/{repo}/download_statistics/detail"
    response = requests.get(url, params=params)
    return response.json()


if __name__ == '__main__':
    func()
