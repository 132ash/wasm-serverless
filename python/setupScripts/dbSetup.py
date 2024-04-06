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
DB_NAME = config.DATA_TRANSFER_DB
couch = couchdb.Server(couchdb_url)


print(f"change max fize to {MAX_FILE_SIZE}.")
configURL = couchdb_url+"/_node/_local/_config/"
response = requests.put(configURL+"/chttpd/max_http_request_size", data=f'"{MAX_FILE_SIZE}"')
print(f"{response.text}, status {response.status_code}")
response = requests.put(configURL+"/couchdb/max_document_size", data=f'"{MAX_FILE_SIZE}"')
response = requests.get(configURL)


# db.create('workflow_latency')
print("create db results,latency and log.")
couch.create('results')
couch.create('latency')
couch.create('log')

print("store text files.")
FILE_NAME = "pg-being_ernest.txt"
FILE_NAME_TEST = "test.txt"
FILE_PATH = "/home/ash/wasm/wasm-serverless/python/setupScripts/text/pg-being_ernest.txt"
with open(FILE_PATH, 'r') as f:
    txt_string = f.read()
    print(len(txt_string))

txt_string_test = "hello the world hello hello sdawe wea w wear e ea fewst ea twe"
if DB_NAME in couch:
    couch.delete(DB_NAME)
couch.create(DB_NAME)
db = couch[DB_NAME]
if FILE_NAME in db:
    doc = db[FILE_NAME]
    db.delete(doc)
db[FILE_NAME] = {"content": txt_string}
db[FILE_NAME_TEST] = {"content": txt_string_test}

print("test fetch file.")
doc = couch[DB_NAME][FILE_NAME]
if 'content' in doc:
    string = doc['content']
    print(f"file length:{len(string)}")
    print(f"part of file content:{string[0:30]}")