import couchdb
import time
import sys

sys.path.append('./config')
import config

couchdb_url = config.COUCH_DB_URL
time.sleep(2)
db = couchdb.Server(couchdb_url)
# db.create('workflow_latency')
db.create('results')
db.create('log')
