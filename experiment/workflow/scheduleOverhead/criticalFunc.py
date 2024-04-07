from typing import List
import couchdb
import sys
from workflowParser import Parser
sys.path.append('../../../config')
import config

workflow = []
db = couchdb.Server(config.COUCH_DB_URL)
mxdis = 0
ans = []

def dfs(name, dis, path: List, timedict):
    global mxdis, ans
    path.append(name)
    tmpdis = dis
    if name in timedict:
        tmpdis = dis + timedict[name]
    if tmpdis > mxdis:
        mxdis = tmpdis
        ans = list(path)
    for name in workflow.nodes[name].prev:
        dfs(name, tmpdis, path, timedict)
    path.pop()

def analyze(workflow_name, timedict):
    global workflow
    parser = Parser(workflow_name)
    workflow = parser.parse()
    for name, _ in workflow.nodes.items():
        if name in timedict:
            dfs(name, 0, [], timedict)
    return ans
