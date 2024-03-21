import yaml
import os

# data structure for function info
function_info_path = '/home/ash/wasm/wasm-serverless/experiment/wasm/docker/func_info.yaml'

class FunctionInfo:
    def __init__(self, function_name, img_name, max_workers, expireTime):
        self.function_name = function_name
        self.img_name = img_name
        self.max_workers = max_workers
        self.expireTime = expireTime

def parse():
    function_info = []
    with open(function_info_path, 'r') as f:
        config = yaml.safe_load(f)
        max_workers = config['max_workers']
        expireTime = config['expireTime']
        for c in config['functions']:
            function_name = c['name']
            img_name = c['image']
            
            # clear previous containers.
            # print("Clearing previous containers.")
            # os.system('docker stop $(docker ps -a | grep \"' + 'image_' + function_name + '\" | awk \'{print $1}\')')
            # os.system('docker rm $(docker ps -a | grep \"' + 'image_' + function_name  + '\" | awk \'{print $1}\')')

            # print("generate:", function_name)
            # packages = c['packages'] if 'packages' in c else [] 
            #generate_image(config_path, function_name, packages)
            
            info = FunctionInfo(function_name,
                              img_name,
                              int(max_workers),
                              expireTime)
            print('img_name', info.img_name)
            function_info.append(info)
    return function_info
