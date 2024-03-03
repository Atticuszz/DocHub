
1. run `sudo apt-get update` got

```bash
root@Atticus-zhou:/home/atticuszz# sudo apt-get update
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease           Hit:2 https://download.docker.com/linux/ubuntu jammy InRelease   Hit:3 https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64  InRelease
Hit:4 http://security.ubuntu.com/ubuntu jammy-security InRelease                                                           Hit:5 https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu jammy InRelease
Hit:6 http://archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:7 http://archive.ubuntu.com/ubuntu jammy-backports InRelease
Traceback (most recent call last):
  File "/usr/lib/cnf-update-db", line 3, in <module>
    import apt_pkg
ModuleNotFoundError: No module named 'apt_pkg'
Reading package lists... Done
E: Problem executing scripts APT::Update::Post-Invoke-Success 'if /usr/bin/test -w /var/lib/command-not-found/ -a -e /usr/lib/cnf-update-db; then /usr/lib/cnf-update-db > /dev/null; fi'
E: Sub-process returned an error code
```

- solved by following

```bash
cd /usr/lib/python3/dist-packages
ls -la | grep "apt_pkg.cpython"
-> -rw-r--r--  1 root root 347096 Aug  2  2023 apt_pkg.cpython-310-x86_64-linux-gnu.so
# then cp that apt_pkg.cpython-310-x86_64-linux-gnu.so
 sudo cp apt_pkg.cpython-310-x86_64-linux-gnu.so apt_pkg.so
```
