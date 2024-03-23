import couchdb
import time
import sys

sys.path.append('/home/ash/wasm/wasm-serverless/python/config')
import config

couchdb_url = config.COUCH_DB_URL
db = couchdb.Server(couchdb_url)
# db.create('workflow_latency')
db.create('results')
db.create('log')
