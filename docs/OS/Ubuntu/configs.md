> ubuntu could be install via usb or wsl

## install system

### usb

- official tutorial[Install Ubuntu desktop | Ubuntu](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview)

1. download `ios file` [Download Ubuntu Desktop | Download | Ubuntu](https://ubuntu.com/download/desktop)
2. download `Flash OS images app`[balenaEtcher - Flash OS images to SD cards & USB drives](https://etcher.balena.io/)
3. let device start by the **flashed** drivers

### wsl

- in Microsoft Store download `wsl` and `ubuntu 22`

### connection

connect by vscode or gateway,wsl mode or ssh

#### wsl

> before connection

remember to set default user as root for more power [set root](docs/OS/Ubuntu/wsl#set default user as root)
_optional: if docker installed ,set default wsl distro as ubuntu 22 by [set default distro](docs/OS/Ubuntu/wsl#set default distro)_

#### native ubuntu

*upgrade power*
1. add into `sudo` group
```bash
sudo usermod -aG sudo yourusername
# check it
groups yourusername
```
2. avoid be asked input passwd call `sudo` everytime
```bash
sudo visudo
# fine the line begin with %sudo and replace it 
%sudo ALL=(ALL) NOPASSWD: ALL
```

[ssh](docs/OS/Ubuntu/net#install ssh)
connect by ssh ,enter password first time and try to connect by ssh-key

## initialization

### set proxies

> before any download from web, set proxies first for too slow speed

#### wsl

[proxy](docs/OS/Ubuntu/wsl#proxy)

1. set shared proxies first!!

#### native ubuntu

1. run clash itself by [clash](docs/OS/Ubuntu/net#clash)
2. or in the same subnet ,share your clash proxy by open allow lan

### basic web tools

```bash
sudo apt update
sudo apt upgrade
sudo apt install net-tools
sudo apt install curl
sudo apt-get update
sudo apt-get install unzip
```

### shell

1. install `zsh` for friendly development experience [zsh](docs/OS/Ubuntu/shell#install zsh)
2. set auto read envs [auto read env](docs/OS/Ubuntu/shell#auto read envs)

### code envs

[code_env](../../../docs/OS/Ubuntu/code_env.md)

- python, conda ,pip, poetry ,cmake...
