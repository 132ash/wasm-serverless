from typing import Dict

class Function:
    def __init__(self, name, prev, next, nextDis, source, runtime, conditions, output=[], traverse=[], split=0):
        self.name = name
        self.prev = prev
        self.next = next
        self.nextDis = nextDis
        self.source = source
        self.runtime = runtime
        self.conditions = conditions
        self.scale = 0
        self.output = output
        self.traverse = traverse
        self.split = split
    
    def set_scale(self, scale):
        self.scale = scale

    def __str__(self):
        return self.name

class Workflow:
    def __init__(self, workflowName, startFunctions, nodes: Dict[str, Function], total, parentCnt):
        self.workflowName:str = workflowName
        self.startFunctions = startFunctions
        self.nodes = nodes  # dict: {name: function()}
        self.total = total
        self.parent_cnt = parentCnt  # dict: {name: parent_cnt}

    def __str__(self):
        workflowName = f"workflow name:{self.workflowName}" 
        startFunctions = f"start functions:{self.startFunctions}" 
        nodes = f"nodes:{self.nodes}" 
        total = f"total functions:{self.total}" 
        parent_cnt = f"parent cnt of functions:{self.parent_cnt}"
        return workflowName+'\n'+startFunctions+'\n'+nodes+'\n'+total+'\n'+parent_cnt
