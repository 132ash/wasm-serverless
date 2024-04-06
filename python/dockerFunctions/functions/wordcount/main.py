import json

def main():
    lis = slice.split()
    countRes = {}
    for word in lis:
        countRes[word] = countRes.get(word, 0) + 1
    return {"countRes": json.dumps(countRes)}
