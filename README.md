# gitcode-migrate-script
gitcode migrate script


# 执行脚本顺序
1. get_webhooks                      done
2. lock_gitee_repos.py               done
该bk, 转移                            done
3. sync_branch_attr.py               done
4. update_gitcode_branch_attr.py     done
5. get_gitcode_webhooks.py           done
6. invite_to_repo.py    # 不涉及
7. cron_sync_repo_member.py   # 不涉及
8. 删除管理员                          done
8. update_repo_attr.py               done
10. 公私仓核对

