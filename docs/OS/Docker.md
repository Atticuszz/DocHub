### install docker and - compose

```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
# add GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# set docker repo
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
# install docker engine
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
# start docker
sudo systemctl start docker
sudo systemctl enable docker
# install docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# check
docker-compose --version
```

```bash
sudo usermod -aG docker username
```
