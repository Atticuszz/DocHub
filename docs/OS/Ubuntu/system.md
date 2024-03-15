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

#### apt source change

```bash
sudo nano /etc/apt/sources.list
sudo apt update
sudo apt upgrade

```
