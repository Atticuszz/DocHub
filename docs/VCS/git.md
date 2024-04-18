## init

### auth

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
# 以下确保在初次安装时候应该正确的内容
git config --global init.defaultBranch main
git config credential.helper
```

### proxy

#### http\\https

```bash

# 与clash一致 设置👌 win
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
# ubuntu in wsl ip is ipv4 of your win
git config --global http.proxy http://192.168.0.107:7890
git config --global https.proxy http://192.168.0.107:7890
```

### SSH

_in admin powershell_

#### start ssh-agent

```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
```

#### generate key-pair

```powershell/bash
ssh-keygen -t ed25519 -C "1831768457@qq.com"
```

_in normal powersehll_

#### add ssh-key-pair into ssh-agent

```powershell
ssh-add C:\Users\18317\.ssh\id_ed25519
```

```bash
eval $(ssh-agent -s)
ssh-add /root/.ssh/id_ed25519
```

#### copy id_ed25519.pub into [github_ssh_setting](https://github.com/settings/keys) set auth key type

```powershell
cat ~/.ssh/id_ed25519.pub | clip
```

```bash
cat ~/.ssh/id_ed25519.pub
```

#### test ssh connect by https

```shell
ssh -T -p 443 git@ssh.github.com
```

#### add config

add the following text into `~/.ssh/config`

```bash
nano ~/.ssh/config
```

windows in `c:\user\your_user_name\.ssh\config`

```text
Host github.com
    Hostname ssh.github.com
    Port 443
    User git
```

#### test test ssh connect

_you may need to enter yes as it's requiring to trust connection to github_

```powershell
ssh -T git@github.com
```

## usual commands

### reset http proxy

```bash

git config --global --unset http.proxy
git config --global --unset https.proxy

git config --global --unset core.gitProxy

git config --local --unset http.proxy
git config --local --unset https.proxy

git config --local --unset core.gitProxy

git config --global --unset http."https://github.com".proxy


```

### check info

```bash
# 列出本地配置
git config --global --list
# 只在本地仓库可以
git config --local --list
```

### remote

1. list remote repo

```shell
git remote -v
```

2. add remote

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <remote_repo_URL>
```

3. associate remote

```bash
git push -u origin main
```

4. set https to ssh

```bash
git remote set-url origin <remote_repo_URL>
```

### remove track

```bash
git rm --cached <file_path_or_folder>
# if folder add -r
```

### roll back

```shell
# force roll back some commit
git reset --hard <commit hash>
# force push remote
git push origin main -f
```

### sync from github

```shell
git fetch origin
git reset --hard origin/main
git clean -fd
```

### submodule

1. clone with submodule

```bash
git clone --recurse-submodules <repository-url>
# if forget to with parms --recurse-submodules try following
git submodule update --init --recursive
```

2. add submodule or clone in main as submodule

```bash
git submodule add <repository-url> <sub_repo_relative_path_to_root>
# if no .gitsubmodules appears try it
git submodule update --init --recursive
```

3. remove

```bash
rm -rf thirdparty/gradslam
rm -rf .git/modules/thirdparty/gradslam
git config --remove-section submodule.thirdparty/gradslam
```

## LFS

```
git lfs install
git lfs track "*.onnx"
git add .gitattributes
git add  "<file_path>.onnx"
git commit -m "add extractor model .onnx"
git push origin main
```

## pre-commit

1. clean cache

```bash
pre-commit clean
```
