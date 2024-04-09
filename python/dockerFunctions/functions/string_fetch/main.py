import couchdb
import time

couchdb_url = 'http://132ash:ash020620@192.168.35.132:5984'
DB_NAME = "strings_for_data_transfer"

class Repository:
    def __init__(self):
        self.couch = couchdb.Server(couchdb_url)

    def fetchString(self, size):
        sizes = ['1KB', '10KB', '100KB', '500KB', '1MB', '10MB', '100MB']
        if size not in sizes:
            raise ValueError("size must be one of {sizes}.")
        doc = self.couch[DB_NAME][size]
        return doc['content']



def main():
    inFuncTIme = time.time()
    repo = Repository()
    res = repo.fetchString(size_DB)
    ready = time.time()
    length = len(res)
    return {"inFuncTIme":inFuncTIme, "readyTime": ready, "strLen":length}
