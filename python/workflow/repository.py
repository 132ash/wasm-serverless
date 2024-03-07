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
        for item in db:
            functions.append(db[item]['function_name'])
        return functions

    def getStartFunctions(self, workflowName):
        dbName = workflowName + '_workflow_metadata'
        db = self.couch[dbName]
        for item in db:
            doc = db[item]
            if 'start_functions' in doc:
                return doc['start_functions']
        
    def createRequestDoc(self, requestId: str) -> None:
        if requestId in self.couch['results']:
            doc = self.couch['results'][requestId]
            self.couch['results'].delete(doc)
        self.couch['results'][requestId] = {}

    def saveWorkflowRes(self, requestId, res):
        self.couch['results'][requestId] = res

    def getWorkflowRes(self, requestId: str):
        return self.couch['results'][requestId]
    