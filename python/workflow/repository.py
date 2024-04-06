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
        containers = {}
        for item in db:
            name = db[item]['function_name']
            source = db[item]['source']
            container = db[item]['container']
            functions.append(db[item]['function_name'])
            sources[name] = source
            containers[name] = container
        return (functions, sources, containers)

    def getStartFunctions(self, workflowName):
        dbName = workflowName + '_workflow_metadata'
        db = self.couch[dbName]
        for item in db:
            doc = db[item]
            if 'start_functions' in doc:
                return doc['start_functions']

    def saveWorkflowRes(self, requestID, res):
        if requestID in self.couch['results']:
            doc = self.couch['results'][requestID]
            self.couch['results'].delete(doc)
        self.couch['results'][requestID] = {'result':res}

    def getWorkflowRes(self, requestID: str):
        doc = self.couch['results'][requestID]
        if 'result' in doc:
            return doc['result']
        # return doc

    def updateLatency(self, requestID: str, latancy:dict):
        if requestID not in self.couch['latency']:
            self.couch['latency'][requestID]  = {'latency':{}}
        doc = self.couch['latency'][requestID]
        doc['latency'].update(latancy)
        self.couch['latency'][requestID] = doc

        
    def getLatency(self, requestID: str):
        return self.couch['latency'][requestID]['latency']

    def clearDB(self, requestID):
        db = self.couch['results']
        db.delete(db[requestID])
