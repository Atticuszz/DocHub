- 简化版 *都在powershell中完成*
]
*system: win11*
### in admin powershell 
#### start ssh-agent
```powershell
Get-Service -Name ssh-agent | Set-Service -StartupType Manual
Start-Service ssh-agent
```
#### generate key-pair
```powershell
ssh-keygen -t ed25519 -C "1831768457@qq.com"
```

### in normal powersehll
#### add ssh-key-pair into ssh-agent
```powershell
ssh-add C:\Users\18317\.ssh\id_ed25519
```

#### copy id_ed25519.pub into  [github_ssh_setting](https://github.com/settings/keys) set auth key type
```powershell
cat ~/.ssh/id_ed25519.pub | clip
```

#### test test ssh connect  
*you may need to enter yes as it's requiring to trust connection to github*
```powershell
ssh -T git@github.com
```

--------------

*以下转自GitHub[生成新的 SSH 密钥并将其添加到 ssh-agent - GitHub 文档](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)*

# 生成新的 SSH 密钥并将其添加到 ssh-agent

## 本文内容

- [关于 SSH 密钥密码](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#about-ssh-key-passphrases)
- [生成新 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)
- [将 SSH 密钥添加到 ssh-agent](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent)
- [为硬件安全密钥生成新的 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key-for-a-hardware-security-key)
检查现有 SSH 密钥后，您可以生成新 SSH 密钥以用于身份验证，然后将其添加到 ssh-agent。
## Platform navigation

- [Mac](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=mac)
- [Windows](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=windows)
- [Linux](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux)

## [关于 SSH 密钥密码](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#about-ssh-key-passphrases)

可以使用 SSH（安全外壳协议）访问和写入 GitHub.com 上的存储库中的数据。 通过 SSH 进行连接时，使用本地计算机上的私钥文件进行身份验证。 有关详细信息，请参阅“[关于 SSH](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/about-ssh)”。

生成 SSH 密钥时，可以添加密码以进一步保护密钥。 每当使用密钥时，都必须输入密码。 如果密钥具有密码并且你不想每次使用密钥时都输入密码，则可以将密钥添加到 SSH 代理。 SSH 代理会管理 SSH 密钥并记住你的密码。

如果您还没有 SSH 密钥，则必须生成新 SSH 密钥用于身份验证。 如果不确定是否已经拥有 SSH 密钥，您可以检查现有密钥。 有关详细信息，请参阅“[检查现有 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/checking-for-existing-ssh-keys)”。

如果要使用硬件安全密钥向 GitHub 验证，则必须为硬件安全密钥生成新的 SSH 密钥。 使用密钥对进行身份验证时，您必须将硬件安全密钥连接到计算机。 有关详细信息，请参阅 [OpenSSH 8.2 发行说明](https://www.openssh.com/txt/release-8.2)。

## [生成新 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key)

可在本地计算机上生成新的 SSH 密钥。 生成密钥后，可以将公钥添加到你在 GitHub.com 上的帐户，以启用通过 SSH 进行 Git 操作的身份验证。

注意：GitHub 通过在 2022 年 3 月 15 日删除旧的、不安全的密钥类型来提高安全性。

自该日期起，不再支持 DSA 密钥 (`ssh-dss`)。 无法在 GitHub.com上向个人帐户添加新的 DSA 密钥。

2021 年 11 月 2 日之前带有 `valid_after` 的 RSA 密钥 (`ssh-rsa`) 可以继续使用任何签名算法。 在该日期之后生成的 RSA 密钥必须使用 SHA-2 签名算法。 一些较旧的客户端可能需要升级才能使用 SHA-2 签名。

1. 打开Git Bash。
    
2. 粘贴以下文本，将示例中使用的电子邮件替换为 GitHub 电子邮件地址。
    
    ```shell
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
    
    注意：如果你使用的是不支持 Ed25519 算法的旧系统，请使用以下命令：
    
    ```shell
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    
    这将以提供的电子邮件地址为标签创建新 SSH 密钥。
    
    ```shell
    > Generating public/private ALGORITHM key pair.
    ```
    
    当系统提示您“Enter a file in which to save the key（输入要保存密钥的文件）”时，可以按 Enter 键接受默认文件位置。 请注意，如果以前创建了 SSH 密钥，则 ssh-keygen 可能会要求重写另一个密钥，在这种情况下，我们建议创建自定义命名的 SSH 密钥。 为此，请键入默认文件位置，并将 id_ALGORITHM 替换为自定义密钥名称。
    
    ```powershell
    > Enter a file in which to save the key (/c/Users/YOU/.ssh/id_ALGORITHM):[Press enter]
    ```
    
3. 在提示符下，键入安全密码。 有关详细信息，请参阅“[使用 SSH 密钥密码](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases)”。
    
    ```shell
    > Enter passphrase (empty for no passphrase): [Type a passphrase]
    > Enter same passphrase again: [Type passphrase again]
    ```
    

## [将 SSH 密钥添加到 ssh-agent](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent)

在向 ssh 代理添加新的 SSH 密钥以管理您的密钥之前，您应该检查现有 SSH 密钥并生成新的 SSH 密钥。

如果已安装 [GitHub Desktop](https://desktop.github.com/)，可使用它克隆存储库，而无需处理 SSH 密钥。

1. 在新的_管理员提升_终端窗口（PowerShell 或 CMD）中，确保 ssh-agent 正在运行。 可以使用“[使用 SSH 密钥密码](https://docs.github.com/zh/articles/working-with-ssh-key-passphrases)”中的“自动启动 ssh agent”说明，或者手动启动它：
    
    ```powershell
    # start the ssh-agent in the background
    Get-Service -Name ssh-agent | Set-Service -StartupType Manual
    Start-Service ssh-agent
    ```
    
2. 在无提升权限的终端窗口中，将 SSH 私钥添加到 ssh-agent。 如果使用其他名称创建了密钥或要添加具有其他名称的现有密钥，请将命令中的 ided25519 替换为私钥文件的名称。
    
    ```powershell
    ssh-add /c/Users/YOU/.ssh/id_ed25519
    ```
    
3. 将 SSH 公钥添加到 GitHub 上的帐户。 有关详细信息，请参阅“[新增 SSH 密钥到 GitHub 帐户](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)”。
    

## [为硬件安全密钥生成新的 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key-for-a-hardware-security-key)

如果您使用 macOS 或 Linux， 在生成新的 SSH 密钥之前，您可能需要更新 SSH 客户端或安装新的 SSH 客户端。 有关详细信息，请参阅“[错误：未知密钥类型](https://docs.github.com/zh/authentication/troubleshooting-ssh/error-unknown-key-type)”。

1. 将硬件安全密钥插入计算机。
    
2. 打开Git Bash。
    
3. 粘贴以下文本，将示例中使用的电子邮件替换为与 GitHub 中帐户关联的电子邮件地址。
    
    ```powershell
    ssh-keygen -t ed25519-sk -C "your_email@example.com"
    ```
    

注意：如果命令失败，并且你收到错误 `invalid format` 或 `feature not supported,`，则表明你可能在使用不支持 Ed25519 算法的硬件安全密钥。 请输入以下命令。

```shell
 ssh-keygen -t ecdsa-sk -C "your_email@example.com"
```

1. 出现提示时，请触摸硬件安全密钥上的按钮。
    
2. 当提示您“Enter a file in which to save the key（输入要保存密钥的文件）”时，按 Enter 接受默认文件位置。
    
    ```shell
    > Enter a file in which to save the key (/c/Users/YOU/.ssh/id_ed25519_sk):[Press enter]
    ```
    
3. 当提示你输入密码时，请按 Enter。
    
    ```shell
    > Enter passphrase (empty for no passphrase): [Type a passphrase]
    > Enter same passphrase again: [Type passphrase again]
    ```
    
4. 将 SSH 公钥添加到 GitHub 上的帐户。 有关详细信息，请参阅“[新增 SSH 密钥到 GitHub 帐户](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)”。