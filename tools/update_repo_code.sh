#!/bin/bash

# shellcheck disable=SC2034
gitee_url=${1}
gitcode_url=${2}
repo=${3}


base_dir="../data"
current_pwd="$(pwd)"

# shellcheck disable=SC2164
cd $base_dir


if [ -d  "${repo}.git" ];then
  cd "${repo}.git" || exit
  git fetch --all --prune
else
  git clone --mirror ${gitee_url}
  cd "${repo}.git" || exit
fi

git push "${gitcode_url}" --prune --force '+refs/heads/*:refs/heads/*' '+refs/tags/*:refs/tags/*'

cd "${current_pwd}" || exit
