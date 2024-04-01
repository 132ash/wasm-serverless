import re

# text = "Hello the World."
# res = {}
# for w in re.split(r'\W+', text):
#     if w:
#         if w not in res:
#             res[w] = 1
#         else:
#             res[w] += 1

# print(res)

import gevent

res = []
param = [1,2,3]
def func(i, res=[], foreach=False):
    if foreach: 
        res.append(i)
        return
    else:
        return i+1

print(func(2))
jobs = [gevent.spawn(func, i, res, True) for i in param]
gevent.joinall(jobs)
print(res)