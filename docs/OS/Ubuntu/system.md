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


