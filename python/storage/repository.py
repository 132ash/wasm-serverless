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

            
    def saveWorkflowInfo(self, workflowName, workflowInfo):
        dbName = workflowName + '_workflowinfo'
        if dbName in self.couch:
            self.couch.delete(dbName)
        self.couch.create(dbName)
        print("save workflow:{}".format(dbName))
        db = self.couch[dbName]
        db.save({workflowName: workflowInfo})

    def deleteWorkflowInfo(self, workflowName):
        dbName = workflowName + '_workflowinfo'
        if dbName in self.couch:
            self.couch.delete(dbName)

    def getWorkflowInfo(self, workflowName):
        return self.retrieveItem(workflowName + '_workflowinfo', workflowName)
            
    def saveFunctionInfo(self, functionName, info):
        dbName = 'functioninfo'
        functionInfo = {}
        if dbName in self.couch:
            functionInfo = self.retrieveItem(dbName, dbName)
            self.couch.delete(dbName)
        functionInfo[functionName] = info
        self.couch.create(dbName)
        db = self.couch[dbName]
        db.save({dbName: functionInfo})

    def deleteFunctionInfo(self, functionName):
        dbName = 'functioninfo'
        if dbName in self.couch:
            functionInfo = self.retrieveItem(dbName, dbName)
            self.couch.delete(dbName)
        functionInfo.pop(functionName)
        self.couch.create(dbName)
        db = self.couch[dbName]
        db.save({dbName: functionInfo})


    def getFunctionInfo(self, functionName):
        dbName = 'functioninfo'
        functionInfo = self.retrieveItem(dbName, dbName)
        return functionInfo[functionName]

    def retrieveItem(self, dbName, itemName):
        db = self.couch[dbName]
        for item in db:
            doc = db[item]
            if itemName in doc:
                return doc[itemName]

