import couchdb
import sys

sys.path.append('../config')
import config

couchdb_url = config.COUCH_DB_URL

couch = couchdb.Server(couchdb_url)

for i in couch:
    print(i)