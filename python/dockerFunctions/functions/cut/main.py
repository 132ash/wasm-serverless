import time

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
    repo = Repository()
    words = repo.fetchString(text_DB).split()
    total_words = len(words)  # 总单词数
    # 每段应包含的单词数。使用整数除法确定基本大小，并计算需要额外添加一个单词的段数
    words_per_segment, extras = divmod(total_words, sliceNum)
    
    segments = []
    start_index = 0  # 每段的起始索引
    for i in range(sliceNum):
        # 对于前extras个段，每段分配一个额外的单词
        end_index = start_index + words_per_segment + (1 if i < extras else 0)
        segments.append(' '.join(words[start_index:end_index]))
        start_index = end_index  # 更新下一段的起始索引

    return {"slice": segments}
