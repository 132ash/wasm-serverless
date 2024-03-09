import couchdb
import sys

sys.path.append('./config')
import config

couchdb_url = config.COUCH_DB_URL

class Repository:
    def __init__(self):
        self.couch = couchdb.Server(couchdb_url)


    def getAllWorkerAddrs(self, workflowName):
        dbName = workflowName + '_workflow_metadata'
        db = self.couch[dbName]
        for item in db:
            doc = db[item]
            if 'addrs' in doc:
                return doc['addrs']
            
    def getFunctionInfo(self, function_name: str, workflowName: str):
        dbName = workflowName + '_function_info'
        db = self.couch[dbName]
        for item in db.find({'selector': {'function_name': function_name}}):
            return item

    def getWorkflowFunctions(self, workflowName):
        dbName = workflowName + '_function_info'
        db = self.couch[dbName]
        functions = []
        sources = {}
        for item in db:
            name = db[item]['function_name']
            source = db[item]['source']
            functions.append(db[item]['function_name'])
            sources[name] = source
        return (functions, sources)

    def getStartFunctions(self, workflowName):
        dbName = workflowName + '_workflow_metadata'
        db = self.couch[dbName]
        for item in db:
            doc = db[item]
            if 'start_functions' in doc:
                return doc['start_functions']

    def saveWorkflowRes(self, requestId, res):
        if requestId in self.couch['results']:
            doc = self.couch['results'][requestId]
            self.couch['results'].delete(doc)
        self.couch['results'][requestId] = {'result':res}

    def getWorkflowRes(self, requestId: str):
        doc = self.couch['results'][requestId]
        if 'result' in doc:
            return doc['result']
        # return doc