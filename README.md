
## 快捷导航
- **tutorials/:**
  - **VCS/:**
    - **github/:**
        - [SSH_keypair_setup_for_GitHub.md](docs/tutorials/VCS/github/SSH_keypair_setup_for_GitHub.md)
      - [git.md](docs/tutorials/VCS/git.md)
  - **shell/:**
      - [CMD.md](docs/tutorials/shell/CMD.md)
  - **basic_tools/:**
      - [vpn.md](docs/tutorials/basic_tools/vpn.md)
      - [git-install-instruction.md](docs/tutorials/basic_tools/git-install-instruction.md)
      - [README.md](docs/tutorials/basic_tools/README.md)
## 最近修改
### 2023-12-30 Atticus Zhou : vault backup: 2023-12-30 15:54:50
- 🔨 [git.md](docs/tutorials/VCS/git.md)
### 2023-12-30 Atticus Zhou : readme 完善教程
- ✨ [CMD.md](docs/tutorials/shell/CMD.md)
## 其他仓库
- 比如后面有单独的项目GitHub链接

## 使用说明
### 这个仓库是什么？
- 这个仓库如其名，是基于git+github+obsidian的知识仓库，用于共享学习过程中的资料文件，或者相关项目的资料，或者作为其他项目仓库的集中导航入口
### 如何使用？
*默认都是windows 64位系统*
#### 直接访问仓库
- **docs文件**夹下都是共享文档，其余文件夹都是自动化脚本等等配置，有兴趣可以研究，可以直接浏览他们
- **如何上传文件？**![](assets/Pasted%20image%2020231230145332.png)
- **如何下载？**
	- 就像访问自己电脑文件夹一样访问docs中的文件，找到想下载的文件图中按钮下载![](assets/Pasted%20image%2020231230150259.png)
#### 配合本地仓库使用
*git是预先配置*
- git
	- 是什么？
		- **版本控制系统**\(*是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统*\)核心工具
	- 干嘛要装它？
		- 这样，你得任何对指定目录下的文件都会被检测到，一旦commit(提交当前更改)，push(推送到GitHub云端)，obsidian+git插件会自动同步云端其他协作者的修改，这就达到了共同协作
	 - 怎么安装？
		 - [下载链接](https://git-scm.com/download/win) （选这**64-bit Git for Windows Setup.** 这个)
		 - [安装指导](docs/tutorials/basic_tools/git-install-instruction)
	- 安装完之后如何下载github仓库？
		-  克隆仓库命令，选择[你合适的目录下打开命令行](docs/tutorials/shell/CMD)或者执行他 
- https *网速太慢，考虑[开启代理](docs/tutorials/VCS/git)，代理也不行，考虑ssh*
```bash
git clone https://github.com/Atticuszz/KnowledgeHub.git
```
- ssh *需要给自己的计算机和[GitHub账户配置额外的密钥](docs/tutorials/VCS/github/SSH_keypair_setup_for_GitHub),速度更快*
```bash
git clone git@github.com:Atticuszz/KnowledgeHub.git
```
下载完毕之后，你可以使用想往常访问文件夹一样访问

#### 结合本地应用使用
- pycharm  *git需要完成[[docs/tutorials/VCS/git|基本配置]]才可进行推送*
	- 是什么？
		- jetbrains系列的IDE(集成开发环境)，适用于python和常见前端框架vue,reat等等
	- 为什么使用它？
		- 因为他是IDE,常见配套的VCS工具很全面，包括**git clone**,**git commit,git push**,常见的命令都有图形化界面,*避免频繁的输入命令行*
	- 如何使用它克隆仓库？
		- 找到从版本控制获取，英文应该是 from VCS，输入仓库链接就可以了
	- 如何推送到github，而不是手动上传内容
		- 先提交更改![](assets/Pasted%20image%2020231230153401.png)
		- 再推送到GitHub![](assets/Pasted%20image%2020231230153558.png)
	- 如何从github自动更新收到内容
- obsidian
	- 是什么？
		- 是一个笔记知识库管理软件(主要是.md文件，也可以有其他文件pdf之类的)，基于Electron框架编写，有着庞大的生态，因此有各种各样的插件可以解决软件使用过程中的一些小需求，比如obsdian-git插件这就让obsidian可以进行基于GitHub的多人协作，备份文档
	- 怎么安装？
		- [Download - Obsidian](https://obsidian.md/download)
		- 安装完毕之后先不要创建仓库
	- 如何配置？
		- 你到期望的目录下，打开cmd或ps，运行下面的命令，并且选择克隆的目录作为vault(obsidian的仓库打开)
	- 如何提交更改？
		- 先 **ctrl+alt+s**，打开右侧的资源面板，会显示最近修改的文件，点击它可以查看文件修改的具体细节![](assets/Pasted%20image%2020231230113200.png)
		- 根据最近的修改，撰写一条提交信息，用于指示，你这次做了哪些改动，按下**ctrl+k** 会会弹出来一个![](assets/Pasted%20image%2020231230113031.png)选择提交信息之后，obsidian-git会将你的更改推送到GitHub仓库
	 - 如何同步？
		 - 初次打开obsidian或者每五分钟，或者ctrl+alt+p,都会自动同步内容

