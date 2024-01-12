### 代理配置

_假设你的clash已经开启，设置代理的效果才有用_

```bash

# 与clash一致 设置👌
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy https://127.0.0.1:7890
```

### 用户配置和默认分支配置

```bash
git config --global user.name "Atticuszz"
git config --global user.email "1831768457@qq.com"
# 以下确保在初次安装时候应该正确的内容
git config --global init.defaultBranch main
git config credential.helper
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
git config --global --list
# 只在本地仓库可以
git config --local --list
```

```shell
git remote -v
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
