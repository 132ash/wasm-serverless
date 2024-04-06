import json

import couchdb
import time

couchdb_url = 'http://132ash:ash020620@192.168.35.132:5984'
DB_NAME = "strings_for_data_transfer"

class Repository:
    def __init__(self):
        self.couch = couchdb.Server(couchdb_url)

    def fetchString(self, key):
        doc = self.couch[DB_NAME][key]
        return doc['content']



def main():
    wordCount = 0
    for subNum in wordNum:
        wordCount += subNum
    return {"wordCount": wordCount}
