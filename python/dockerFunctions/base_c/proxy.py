import os
import time
import couchdb
import subprocess
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import container_config

default_file = 'main'
work_dir = '/proxy'
couchdb_url = container_config.COUCHDB_URL
# db_server = couchdb.Server(couchdb_url)

class Runner:
    def __init__(self):
        self.code = None
        self.function = None
        self.filePath = ""
        self.ctx = {}

    def init(self, function):
        print('init...')
        os.chdir(work_dir)
        self.function = function
        self.filePath = os.path.join(work_dir, default_file)
        print('init finished...')

    def run(self, param):
        self.ctx = param
        param_list = [str(n) for n in param.values()]
        start = time.time()
        result = subprocess.run([self.filePath]+param_list, capture_output=True, text=True)
        end = time.time()
        if result.returncode == 0:
            # 打印main程序的输出
            res =  result.stdout
        else:
             res = result.stderr
            # 如果有错误，打印错误信息
        print(str(res))
        return {"result":str(res), "time":end-start}


proxy = Flask(__name__)
proxy.status = 'new'
proxy.debug = False
runner = Runner()


@proxy.route('/status', methods=['GET'])
def status():
    res = {}
    res['status'] = proxy.status
    res['workdir'] = os.getcwd()
    if runner.function:
        res['function'] = runner.function
    return res


@proxy.route('/init', methods=['POST'])
def init():
    proxy.status = 'init'

    inp = request.get_json(force=True, silent=True)
    runner.init(inp['function'])

    proxy.status = 'ok'
    return ('OK', 200)


@proxy.route('/run', methods=['POST'])
def run():
    proxy.status = 'run'

    inp = request.get_json(force=True, silent=True)
    # record the execution time
    out = runner.run(inp)
    proxy.status = 'ok'
    return out


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), proxy)
    server.serve_forever()
