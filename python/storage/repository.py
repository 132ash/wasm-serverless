import couchdb
import sys
sys.path.append('../config')
import config

couchdb_url = config.COUCH_DB_URL

class Repository:
    def __init__(self):
        self.couch = couchdb.Server(couchdb_url)
            
    def saveWorkflowInfo(self, workflowName, workflowInfo):
        dbName = workflowName + '_workflowinfo'
        if dbName in self.couch:
            self.couch.delete(dbName)
        self.couch.create(dbName)
        db = self.couch[dbName]
        db.save({workflowName: workflowInfo})

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

