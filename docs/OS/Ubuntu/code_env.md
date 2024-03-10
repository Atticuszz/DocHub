#### install cmake

```bash
sudo apt-get update
sudo apt-get install cmake
cmake --version
```

#### install python

- python 3

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt-get update
sudo apt-get install python3.11-dev
python3.11 --version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --config python3
```

- python pip

```bash
sudo apt update
sudo apt install python3-pip
```

- python venv

```bash
sudo apt update
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
# to get out of current venv
deactivate
```

#### install poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
nano ~/.bashrc
# add it
export PATH="/root/.local/bin:$PATH"
source ~/.bashrc
poetry --version
```

#### install conda

1. install by wget

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
# note it may show that conda installed in /root/miniconda3
```

> remember set no to auto activate in your shell if u use poetry,etc to manage py-env

2. add `/root/miniconda3/bin` to `PATH` in `/etc/environment`

```bash
PATH="/root/miniconda3/bin:"
source /etc/environment
```

3. test conda

```bash
conda info
```

4.  optinal, enable auto activate conda

```bash
conda config --set auto_activate_base true
```

> repeat to warn `conda init` ,try `conda init <shell>`
