import yaml
import sys

sys.path.append('./config')
sys.path.append('./storage')
import config
from repository import Repository

yamlPath = config.WORKFLOWYAMLPATH

class Parser:
    def __init__(self, workflowName):
        self.workflowName = workflowName
        self.yamlData = yaml.load(open(yamlPath+'/'+workflowName+'.yaml'), Loader=yaml.FullLoader)

    def parse(self):
        workflowData = {'switchFunction':{}, 'next':{}, 'type':{}}
        for function in self.yamlData["functions"]:
            if 'start' in function:
                if 'startFunction' in workflowData:
                    raise Exception("Mutiple start function.")
                workflowData['startFunction'] = {'name':function['name']}
            if function['type'] == 'END':
                if 'endFunction' in workflowData:
                    raise Exception("Mutiple end function.")
                endFunction = {}
                endFunction['output'] = function['output']
                workflowData['endFunction'] = endFunction
            if function['type'] == 'SWITCH':
                switchFunction = {}
                switchFunction['output'] = function['output']
                switchFunction['condition'] = function['condition']
                workflowData['switchFunction'][function['name']] = switchFunction
            if 'next' in function:
                workflowData['next'][function['name']] = function['next']
            workflowData['type'][function['name']] = function['type']
        self.workflowData = workflowData
        return workflowData

    def saveWorkflowData(self):
        repo = Repository()
        repo.saveWorkflowInfo(self.workflowName, self.workflowData)

if __name__ == "__main__":
    parser = Parser("workflow")
    data = parser.parse()
    parser.saveWorkflowData()
    data = parser.getWorkflowData()
    print(data)
        