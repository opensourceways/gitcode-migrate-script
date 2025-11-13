#!/bin/bash

# shellcheck disable=SC2034
repo=${1}
owner=${2}
file_name=${3}
file_path=${4}


base_dir="../data"
current_pwd="$(pwd)"
content="# 通知: 本项目已经正式迁移至 [Gitcode](https://gitcode.com/${owner}/${repo}) 平台\n"
# content="# 通知: 本项目已经暂停，CANN相关项目迁移至 [Gitcode](https://gitcode.com/cann) 平台\n"

# shellcheck disable=SC2164
cd ${base_dir}

if [ ! -d "${repo}" ];then
#  git clone --depth 1 git@gitee.com:"${owner}"/"${repo}".git
  git clone --depth 1  https://ascend-ci-bot:***@gitee.com/"${owner}"/"${repo}".git
fi

cd "${repo}" || exit

git pull

if [ -n "${file_path}" ]; then
  cd "${file_path}" || exit
fi


if [ -z "${file_name}" ]; then
  touch README.md
  sed -i "1i $content" README.md
else
  sed -i "1i $content" "${file_name}"
fi

git add .
git commit -m "add migrate note"
git push

cd "${current_pwd}" || exit
