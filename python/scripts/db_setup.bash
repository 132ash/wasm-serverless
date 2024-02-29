apt-get update
apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
apt-get install wondershaper
# install and initialize couchdb
docker pull couchdb
sudo docker run -itd -p 5984:5984 -e COUCHDB_USER=132ash -e COUCHDB_PASSWORD=ash020620 --name couchdb couchdb
pip3 install -r requirements.txt
python3 couchdb_starter.py

sudo docker remove 57ac3a662cfa71ed1f4a9ea9e0246334994515758e396d62059752c512ea2559