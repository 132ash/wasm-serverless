import yaml
import sys

sys.path.append('./config')
sys.path.append('./storage')
import config
import component

yamlPath = config.WORKFLOWYAMLPATH
NETWORK_BANDWIDTH = config.NETWORK_BANDWIDTH

class Parser:
    def __init__(self, workflowName):
        self.workflowName = workflowName
        self.yamlData = yaml.load(open(yamlPath+'/'+workflowName+'.yaml'), Loader=yaml.FullLoader)

    def parse(self) -> component.Workflow:
        start_functions = []
        nodes = dict()
        parent_cnt = dict()
        total = 0
        functions = self.yamlData['functions']
        haveEndFunction = False
        parent_cnt[functions[0]['name']] = 0
        sinkFuncs = []
        for function in functions:
            name = function['name']
            source = function['source']
            runtime = function['runtime']
            container = function.get('container', '')
            next = list()
            nextDis = list()
            send_time = 0
            conditions = list()
            traverse = list()
            output = list()
            if source == 'FOREACH':
                traverse = function['traverse'] 
                if len(function['next']['funcs']) != 1:
                    raise Exception("Mutiple foreach unit.")
            if source == 'END':
                if haveEndFunction:
                    raise Exception("Mutiple end function.")
                output = function['output']  
                haveEndFunction = True
            if 'next' in function:
                send_time = function['next']['size'] / NETWORK_BANDWIDTH
                if function['next']['type'] == 'SWITCH' or function['next']['type'] == 'SINK':
                    conditions = function['next']['conditions']  
                    output = function['output']  
                if function['next']['type'] == 'SINK':
                    sinkFuncs.append(name)
                for next_func in function['next']['funcs']:
                    next.append(next_func)
                    nextDis.append(send_time)
                    if next_func not in parent_cnt:
                        parent_cnt[next_func] = 1
                    else:
                        parent_cnt[next_func] = parent_cnt[next_func] + 1
            current_function = component.Function(name, container, [], next, nextDis, source, 
                                                  runtime,conditions, output, traverse)
            if 'scale' in function:
                current_function.set_scale(function['scale'])
            total = total + 1
            nodes[name] = current_function
        for name in nodes:
            if name not in parent_cnt or parent_cnt[name] == 0:
                parent_cnt[name] = 0
                start_functions.append(name)
            for next_node in nodes[name].next:
                nodes[next_node].prev.append(name)
        for sink in sinkFuncs:
            parent_cnt[sink] = 1
        return component.Workflow(self.workflowName, start_functions, nodes, total, parent_cnt)


if __name__ == "__main__":
    parser = Parser("workflow")
    data = parser.parse()
    print(data)
        