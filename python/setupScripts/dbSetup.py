import os
import couchdb
import time
import sys

sys.path.append('/home/ash/wasm/wasm-serverless/python/config')
import config

print("Flush previous db containers.")
os.system("docker stop $(docker ps -a | grep \"couchdb\" | awk '{print $1}')")
os.system("docker rm $(docker ps -a | grep \"couchdb\" | awk '{print $1 }')")
os.system("docker run -itd -p 5984:5984 -e COUCHDB_USER=132ash -e COUCHDB_PASSWORD=ash020620 --name couchdb couchdb")
print("create db results and log.")
time.sleep(2)
couchdb_url = config.COUCH_DB_URL
db = couchdb.Server(couchdb_url)
# db.create('workflow_latency')
db.create('results')
db.create('log')