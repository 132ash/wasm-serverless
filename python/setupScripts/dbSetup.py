import os
import couchdb
import time
import sys
import requests

MAX_FILE_SIZE = 4294967296 #4GB

sys.path.append('/home/ash/wasm/wasm-serverless/python/config')
import config

print("Flush previous db containers.")
os.system("docker stop $(docker ps -a | grep \"couchdb\" | awk '{print $1}')")
os.system("docker rm $(docker ps -a | grep \"couchdb\" | awk '{print $1 }')")
os.system("docker run -itd -p 5984:5984 -e COUCHDB_USER=132ash -e COUCHDB_PASSWORD=ash020620 --name couchdb couchdb")
time.sleep(2)


couchdb_url = config.COUCH_DB_URL
db = couchdb.Server(couchdb_url)


print(f"change max fize to {MAX_FILE_SIZE}.")
configURL = couchdb_url+"/_node/_local/_config/"
response = requests.put(configURL+"/chttpd/max_http_request_size", data=f'"{MAX_FILE_SIZE}"')
print(f"{response.text}, status {response.status_code}")
response = requests.put(configURL+"/couchdb/max_document_size", data=f'"{MAX_FILE_SIZE}"')
response = requests.get(configURL)
print(f"config: {response.text}")


# db.create('workflow_latency')
print("create db results and log.")
db.create('results')
db.create('log')