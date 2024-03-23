import couchdb
import sys
import random
import string
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config

couchdb_url = config.COUCH_DB_URL
DB_NAME = config.TRANSFER_DB

class Repository:
    def __init__(self, flush_old_db=True):
        self.couch = couchdb.Server(couchdb_url)
        self.strings = {}
        if flush_old_db:
            if DB_NAME in self.couch:
                self.couch.delete(DB_NAME)
        
    #generate all strings. 
    @classmethod
    def makeAndStoreStrings(cls):
        sizes = [1024, 10240, 1048576]  # 以字节为单位
        keys = ['1KB', '10KB', '1MB']
        # 生成随机字符串并存储到字典中
        repo = cls()
        for key, size in zip(keys,sizes):
            # 生成一个随机字符串，大小为size字节
            random_string = ''.join(random.choices(string.ascii_letters, k=size))
            # 将生成的字符串存储到字典中，键为字符串大小
            repo.strings[key] = random_string
        repo.storeStrings()
        return repo

    def storeStrings(self):
        if DB_NAME not in self.couch:
            self.couch.create(DB_NAME)
        db = self.couch[DB_NAME]
        for name, string in self.strings.items():
            if name in db:
                doc = db[name]
                db.delete(doc)
            db[name] = {"content": string}
    

    def fetchString(self, size):
        sizes =  ['1KB', '10KB', '1MB']
        if size not in sizes:
            raise ValueError("size must be one of {sizes}.")
        doc = self.couch[DB_NAME][size]
        if 'content' in doc:
            return doc['content']




if __name__ == "__main__":
    repo = Repository.makeAndStoreStrings()
    for size in ['1KB', '10KB', '1MB']:
        data = repo.fetchString(size)
        print(len(data))
        print(data[1:50])
