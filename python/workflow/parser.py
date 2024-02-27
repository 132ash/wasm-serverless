import yaml
import sys

sys.path.append('../config')
sys.path.append('../storage')
import config
from repository import Repository

yamlPath = config.WORKFLOWYAMLPATH

class Parser:
    def __init__(self, workflowName):
        self.workflowName = workflowName
        self.yamlData = yaml.load(open(yamlPath+'/'+workflowName+'.yaml'), Loader=yaml.FullLoader)

    def parse(self):
        workflowData = {'switchFunction':{}, 'next':{}}
        for function in self.yamlData["functions"]:
            if function['type'] == 'START':
                if 'startFunction' in workflowData:
                    raise Exception("Mutiple start function.")
                workflowData['startFunction'] = function['name']
            if function['type'] == 'END':
                if 'endFunction' in workflowData:
                    raise Exception("Mutiple end function.")
                workflowData['endFunction'] = function['output']
            if function['type'] == 'SWITCH':
                switchFunction = {}
                switchFunction['input'] = function['input']
                switchFunction['output'] = function['output']
                workflowData['switchFunction'][function['name']] = switchFunction
            if 'next' in function:
                nextFunction = {}
                nextFunction['type'] = function['next']['type']
                nextFunction['nodes'] = function['next']['nodes']
                workflowData['next'][function['name']] = nextFunction
        self.workflowData = workflowData
        return workflowData

    def saveWorkflowData(self):
        repo = Repository()
        repo.saveWorkflowInfo(self.workflowName, self.workflowData)
    
    def getWorkflowData(self):
        repo = Repository()
        return repo.getWorkflowInfo(self.workflowName)

if __name__ == "__main__":
    parser = Parser("workflow")
    data = parser.parse()
    parser.saveWorkflowData()
    data = parser.getWorkflowData()
    print(data)
        