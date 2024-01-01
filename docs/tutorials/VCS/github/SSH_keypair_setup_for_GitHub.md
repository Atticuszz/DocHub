- 简化版 *都在powershell中完成*
## SSH
1. generate key-pair
```powershell
ssh-keygen -t ed25519 -C "1831768457@qq.com"
```
2. copy id_rsa.pub into [github_ssh_setting](https://github.com/settings/keys)  set auth key type
```powershell
cat ~/.ssh/id_rsa.pub | clip
```
3. test ssh connect  *you may need to enter yes as it's requiring to trust connection to github*
```powershell
ssh -T git@github.com
```
--------------

*以下转自GitHub[Setup SSH keys for use with GitHub/GitLab/BitBucket etc · GitHub](https://gist.github.com/developius/c81f021eb5c5916013dc)*

### Create a repo.
Make sure there is at least one file in it (even just the README.md)


### Generate a SSH key pair (private/public):
```
ssh-keygen -t rsa -C "your_email@example.com"
```

or even better:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

It also possible to use ed25519. There are pros and cons, but personally I've had some issues and that is the reason I've chosen to stick to 4096 rsa for now.

### Copy the contents of the public SSH key

macOS:
```
pbcopy < ~/.ssh/id_rsa.pub
```
GNU/Linux (requires the xclip package):
```
xclip -sel clip < ~/.ssh/id_rsa.pub
```
Windows Command Line:
```
type %userprofile%\.ssh\id_rsa.pub | clip
```
Git Bash on Windows / Windows PowerShell:
```
cat ~/.ssh/id_rsa.pub | clip
```

or ofcourse copy it via your favorite editor, cat, or whatever suits your needs :)


### Copy the public SSH key to GitHub
Copy the contents of the to your SSH keys to your GitHub account settings (https://github.com/settings/keys).


### Test the SSH key:
```
ssh -T git@github.com
```

Change directory into the local clone of your repository (if you're not already there) and run:
```
git remote set-url origin git@github.com:username/your-repository.git
```

Now try editing a file (try the README) and then do:
```
git add -A
git commit -am "Update README.md"
git push
```

Add the key to the ssh-agent
```
ssh-add ~/.ssh/id_rsa
```

You should not be asked for a username or password. If it works, your SSH key is correctly configured.