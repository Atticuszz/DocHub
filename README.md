
## 快捷导航
- **papers/:**
    - [Point-SLAM Dense Neural Point Cloud-based SLAM.pdf](docs/papers/Point-SLAM%20Dense%20Neural%20Point%20Cloud-based%20SLAM.pdf)
- **tutorials/:**
  - **VCS/:**
    - **github/:**
        - [SSH_keypair_setup_for_GitHub.md](docs/tutorials/VCS/github/SSH_keypair_setup_for_GitHub.md)
      - [git.md](docs/tutorials/VCS/git.md)
  - **shell/:**
      - [CMD.md](docs/tutorials/shell/CMD.md)
      - [powershell.md](docs/tutorials/shell/powershell.md)
    - [KnowledgeHub.md](docs/tutorials/KnowledgeHub.md)
  - **basic_tools/:**
      - [vpn.md](docs/tutorials/basic_tools/vpn.md)
      - [git-install-instruction.md](docs/tutorials/basic_tools/git-install-instruction.md)
      - [README.md](docs/tutorials/basic_tools/README.md)
- **C++/:**
  - **STL/:**
      - [set.md](docs/C++/STL/set.md)
      - [unordered_map.md](docs/C++/STL/unordered_map.md)
      - [algorithm.md](docs/C++/STL/algorithm.md)
      - [stack.md](docs/C++/STL/stack.md)
      - [unordered_set.md](docs/C++/STL/unordered_set.md)
      - [Queue.md](docs/C++/STL/Queue.md)
      - [vector.md](docs/C++/STL/vector.md)
      - [String.md](docs/C++/STL/String.md)
      - [map.md](docs/C++/STL/map.md)
    - [syntax.md](docs/C++/syntax.md)
  - [meetings.md](docs/meetings.md)
## 最近修改
### 2024-01-12 by zsqgle - Update vpn.md
- 🔨 [vpn.md](docs/tutorials/basic_tools/vpn.md)
### 2024-01-09 by Atticuszz - 去除了仓库的python代码，直接通过自动话脚本命令行
- 🔨 [meetings.md](docs/meetings.md)
### 2024-01-09 by Atticuszz - Update README.md automatically
- 🔨 [KnowledgeHub.md](docs/tutorials/KnowledgeHub.md)
### 2024-01-09 by Atticuszz - 1. 移动使用仓库的教程到单独的文件 2. 增加了pycharm自动拉取仓库的教程 3. 添加了下一次会议的主题和准备材料需求
- ✨ [meetings.md](docs/meetings.md)
- ✨ [KnowledgeHub.md](docs/tutorials/KnowledgeHub.md)
### 2024-01-04 by Atticuszz - 2024-01-04 21:40:19: powershell 杀掉 占用进程命令
- ✨ [powershell.md](docs/tutorials/shell/powershell.md)
### 2024-01-04 by Atticuszz - 增加了git常见命令
- 🔨 [git.md](docs/tutorials/VCS/git.md)
## 其他仓库
### 论文速览
1. [GitHub - eriksandstroem/Point-SLAM: Point-SLAM: Dense Neural Point Cloud-based SLAM](https://github.com/eriksandstroem/Point-SLAM)
	- ![](https://github.com/eriksandstroem/Point-SLAM/raw/main/media/office_4.gif)
2. [GitHub - youmi-zym/GO-SLAM: [ICCV2023] GO-SLAM: Global Optimization for Consistent 3D Instant Reconstruction](https://github.com/youmi-zym/GO-SLAM)
	- ![](https://github.com/youmi-zym/GO-SLAM/raw/main/images/comparison.png)
3. [GitHub - HengyiWang/Co-SLAM: [CVPR'23] Co-SLAM: Joint Coordinate and Sparse Parametric Encodings for Neural Real-Time SLAM](https://github.com/HengyiWang/Co-SLAM)
	- ![https://github.com/HengyiWang/Co-SLAM/raw/main/media/coslam_teaser.gif](https://github.com/HengyiWang/Co-SLAM/raw/main/media/coslam_teaser.gif)

**[仓库使用教程](docs/tutorials/KnowledgeHub)**

### 常见问题和禁忌
#### 合并远程内容失败
- 当前仓库目录下运行
```PowerShell
git stash           # 保存未提交的更改
git fetch --all
git reset --hard origin/main
git stash pop       # 重新应用之前保存的更改
```
#### 文件命名目录名要求
1. 尽量不要有空格，空格会影响markdown链接的生成
2. 尽量不要用中文命名，不知道用哪个单词先搜一下，养成英文环境的好习惯
#### 大文件不要放到仓库
- 大文件100mb以上的需要使用git-lfs来推送  *或者直接放在release页面，单独上传文件*