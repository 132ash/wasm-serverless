import yaml
import sys

sys.path.append('../../config')
import config

yamlPath = config.WORKFLOWYAMLPATH
workflowName = 'workflow'

data = yaml.load(open(yamlPath+'/'+workflowName+'.yaml'), Loader=yaml.FullLoader)

functions = data['functions']
for function in functions:
    print(function['input'])