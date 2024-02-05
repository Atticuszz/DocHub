## <font color="#4bacc6"> VSCode连接</font>

![[assets/1ffa2d81edf7f1dece8d86f71f4b57f.png]]
首先点开左下角连接按钮，如果没有安装ssh的插件按照软件提示安装

在本地使用命令新建密匙，具体操作步骤见（SSH_keypair_setup_for_GitHub）创建密匙，在配置config中放入私钥，将公钥（带pub后缀）放入服务器/root/.ssh/authorized_key中，vscode里面config不带pub后缀，里面放的是私钥

VSCode打开C:\Users\your_user_name\.ssh里面的config文件，添加内容：
```
Host 8606fd5959.vicp.fun</font>
    User root
    Port 28215
    IdentityFile <这个应该是你的id_ed25519绝对路径>
```
密匙名称根据不同的加密方式有所差别
8606fd5959.vicp.fun为服务器域名，28215这是ssh端口，如果到时候连接树莓派，用termius和vscode，都是这么连接。

配置完成后，按图点击链接
![[assets/1ffa2d81edf7f1dece8d86f71f4b57f 2.png]]
![[assets/530bcd1287b9daae311bd6a7d0d8f6e 1.png]]
![[assets/c289f87ef103efb2964dd7c4dacb4e9.png]]
![[assets/c68058356f448e566b6677b9455f17a 1.png]]