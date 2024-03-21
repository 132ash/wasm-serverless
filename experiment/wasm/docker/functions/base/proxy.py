import os
import time
import couchdb
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import container_config

default_file = 'main.py'
work_dir = '/proxy'
couchdb_url = container_config.COUCHDB_URL
# db_server = couchdb.Server(couchdb_url)

class Runner:
    def __init__(self):
        self.code = None
        self.function = None
        self.ctx = {}

    def init(self, function):
        print('init...')
        os.chdir(work_dir)
        self.function = function

        # compile first
        filename = os.path.join(work_dir, default_file)
        with open(filename, 'r') as f:
            self.code = compile(f.read(), filename, mode='exec')

        print('init finished...')

    def run(self, param):
        # FaaSStore
        self.ctx = param

        # pre-exec
        exec(self.code, self.ctx)

        # run function
        out = eval('main()', self.ctx)


        return out


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
    start = time.time()
    out = runner.run(inp)
    end = time.time()

    res = {
        "start_time": start,
        "end_time": end,
        "out": out
    }

    proxy.status = 'ok'
    return res


if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 5000), proxy)
    server.serve_forever()
