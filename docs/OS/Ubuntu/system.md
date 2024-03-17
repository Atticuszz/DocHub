### system

#### ignore lid switch

```bash
sudo nano /etc/systemd/logind.conf
# make sure
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
# then run
sudo systemctl restart systemd-logind
```

#### gui

> no test

```bash
sudo apt update
sudo apt full-upgrade
sudo apt install --no-install-recommends xserver-xorg
sudo apt install --no-install-recommends xinit
sudo apt install raspberrypi-ui-mods
sudo apt install --no-install-recommends lightdm
```

#### qt

```bash
sudo apt-get update
sudo apt-get install qtbase5-dev
```

#### change password

```powershell
# admin
wsl -u root
passwd %username% # empty for root
```

#### upgrade to root

```shell
usermod -aG sudo %username%
sudo chown -R %username%  %filepath%
# sudo chown -R atticuszz /etc/

```

### basic tools for desktop

#### use eye protection mode

setting-> display-> night light

#### snap shop update

```bash
sudo snap refresh snap-store
sudo snap refresh
```

#### keyboard

```bash
sudo apt-get update
sudo apt-get install ibus ibus-pinyin ibus-libpinyin
```

#### system backup

```bash
sudo apt-get update
sudo apt-get install timeshift
```

#### clipboard

```bash
sudo apt update
sudo apt install copyQ
```

#### gpu monitor

```bash
conda install -c conda-forge nvitop
```

#### fan mode

use `Legion` in windows to set mode

#### screenshot

[Snipaste Downloads](https://www.snipaste.com/download.html)

```bash
sudo apt-get update
sudo apt-get install fuse
chmod +x /home/atticuszz/Downloads/Snipaste-2.8.9-Beta-x86_64.AppImage
/home/atticuszz/Downloads/Snipaste-2.8.9-Beta-x86_64.AppImage --appimage-extract
# create desktop app then
mkdir -p ~/.config/autostart/
cp ~/Desktop/Snipaste.desktop ~/.config/autostart/
```

#### install .tar.gz

```bash
tar -xzf filepath
```

#### apt source change

```bash
sudo nano /etc/apt/sources.list
sudo apt update
sudo apt upgrade

```

### flathub

[Ubuntu Flathub Setup | Flathub](https://flathub.org/setup/Ubuntu)

#### Linux System Optimizer & Monitoring

```bash
flatpak install flathub net.nokyan.Resources
```

#### Dual system extend disk for ubunut

[Windows + Linux(Ubuntu)双系统扩展Linux磁盘空间\_双系统下 windows 为 ubuntu 扩充新空间 | linux 扩容原理介绍 + 填坑-CSDN博客](https://blog.csdn.net/jayoungo/article/details/105598613#:~:text=Windows%20%2B%20Linux%20%28Ubuntu%29%E5%8F%8C%E7%B3%BB%E7%BB%9F%E6%89%A9%E5%B1%95Linux%E7%A3%81%E7%9B%98%E7%A9%BA%E9%97%B4%201%20%E9%87%8D%E8%A6%81%EF%BC%81%201.%20%E6%89%A7%E8%A1%8C%E7%A1%AC%E7%9B%98%E5%88%86%E5%8C%BA%E4%BF%AE%E6%94%B9%E6%93%8D%E4%BD%9C%E5%89%8D%E5%BB%BA%E8%AE%AE%E5%A4%87%E4%BB%BDWindows%E5%8F%8ALinux%E7%B3%BB%E7%BB%9F%E9%87%8D%E8%A6%81%E6%96%87%E4%BB%B6%EF%BC%8C%E4%BB%A5%E9%98%B2%E6%93%8D%E4%BD%9C%E5%A4%B1%E8%B4%A5%E5%AF%BC%E8%87%B4,%E6%8F%92%E5%85%A5%E6%AD%A5%E9%AA%A4%E4%B8%80%E5%88%9B%E5%BB%BA%E7%9A%84%E5%8F%AF%E5%90%AF%E5%8A%A8U%E7%9B%98%202.%20...%205%20%E5%8F%82%E8%80%83%E8%B5%84%E6%96%99%20http%3A%2F%2Fjoejanuszk.com%2Fblog%2Fincreasing-ubuntu-partition-size-dual-boot-windows%20%E6%96%87%E7%AB%A0%E5%9C%B0%E5%9D%80%EF%BC%9Ahttps%3A%2F%2Fblog.csdn.net%2Fjayoungo%2Farticle%2Fdetails%2F105598613%20%E8%BD%AC%E8%BD%BD%E8%AF%B7%E6%B3%A8%E6%98%8E%E5%87%BA%E5%A4%84%E3%80%82)

#### increase swap space via swap file
<<<<<<< HEAD
*extend to 16gb for example*
[How to increase swap space? - Ask Ubuntu](https://askubuntu.com/questions/178712/how-to-increase-swap-space)
=======

_extend to 16gb for example_

>>>>>>> origin/main
```bash
sudo swapoff -a
sudo fallocate -l 16G /swapfile
# if failed fallocate try
sudo dd if=/dev/zero of=/swapfile bs=1G count=16

# then
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make it permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
# test it
swapon --show
->
❯ swapon --show

NAME      TYPE SIZE USED PRIO
/swapfile file  16G   0B   -2
```
