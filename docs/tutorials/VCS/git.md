### 代理配置
*假设你的clash已经开启，设置代理的效果才有用*
```bash

# 与clash一致 设置👌
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```
### 用户配置和默认分支配置
```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
git config --global init.defaultBranch main
```