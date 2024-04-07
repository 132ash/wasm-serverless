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

    def saveLatency(self, requestID: str,funcName:str, latancy:dict):
        latency_db = self.couch['latency']
        latency_db.save({'requestID':requestID, 'funcName':funcName, 'latancy':latancy})

        
    def getLatency(self, requestID: str):
        latency = {}
        for _id in self.couch['latency']:
            doc = self.couch['latency'][_id]
            if doc['requestID'] == requestID:
                latency[doc['funcName']] = doc['latancy']
        return latency

    def clearDB(self, requestID):
        db = self.couch['results']
        db.delete(db[requestID])
        for _id in self.couch['latency']:
            doc = self.couch['latency'][_id]
            if doc['requestID'] == requestID:
                self.couch['latency'].delete(doc)
