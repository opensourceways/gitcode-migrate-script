# 配置

# ============================ Role ========================
BoostKitDEV = ""
CannDEV = ""
AscendDev = ""
AscendMirrorDev = ""


# ============================ Gitee ========================
# ascend-ci-bot
GiteeV5Token = ""  # 企业V5 token
GiteeV8Token = ""  # 企业V8 token
GiteePWD = "!"  # Gitee 密码
# yao-xiaobai
# GiteeV5Token = ""  # 企业V5 token
# GiteeV8Token = ""  # 企业V8 token
# GiteePWD = ""  # Gitee 密码

# ============================ Gitcode ========================
GitcodeAccessToken = "-"
GitcodeClientID = ""
GitcodeHeaderCookie = "=; ="

# ============================ Gitee ========================
# 锁仓相关
StrReadmeAddContent = "# 通知: 本项目已经正式迁移至 [Gitcode](https://gitcode.com/{owner}/{repo}) 平台\n"  # 修改 readme文件
# StrReadmeAddContent = "# 通知: 本项目已经暂停，CANN相关项目迁移至 [Gitcode](https://gitcode.com/cann) 平台\n"
DirName = ".本项目已经正式迁移至 Gitcode 平台/README.md"  # 新增目录

X_Csrf_Token = ""
Cookie = ""

# ============================ Gitcode ========================
# Gitcode web-api 请求头
Bearer = ""

GitCodeRequestHeaders = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": f"Bearer {Bearer}",
    "gitcode-utm-source": "",
    "page-ref": "https%3A%2F%2Fgitcode.com%2Forg%2Fascend-mirror%2Fenterprise%2FrolesPermission",
    "page-title": "%E4%BC%81%E4%B8%9A%E8%AE%BE%E7%BD%AE",
    "page-uri": "https%3A%2F%2Fgitcode.com%2Forg%2Fascend-mirror%2Fenterprise%2Fmember",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-app-channel": "gitcode-fe",
    "x-app-version": "0",
    "x-device-id": "unknown",
    "x-device-type": "Windows",
    "x-network-type": "4g",
    "x-os-version": "10",
    "x-platform": "web",
    "referer": "https://gitcode.com/"
}
