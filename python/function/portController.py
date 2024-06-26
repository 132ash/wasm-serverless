from gevent.lock import BoundedSemaphore

class PortController:
    def __init__(self, min_port_wasm, max_port_wasm, min_port_docker, max_port_docker):
        self.portlock = {"wasm":BoundedSemaphore(), 'docker':BoundedSemaphore()}
        self.wasm_port_resource = list(range(min_port_wasm, max_port_wasm))
        self.docker_port_resource = list(range(min_port_docker, max_port_docker))

    def get(self, type):
        self.portlock[type].acquire()
        if type == 'wasm':  
            if len(self.wasm_port_resource) == 0:
                raise Exception("no idle port")
            port = self.wasm_port_resource.pop(0)
        else:  
            if len(self.docker_port_resource) == 0:
                raise Exception("no idle port")
            port = self.docker_port_resource.pop(0)
        self.portlock[type].release()
        return port

    def put(self, port, type):
        self.portlock[type].acquire()
        if type == 'wasm':  
            self.wasm_port_resource.append(port)
        else:  
            self.docker_port_resource.append(port)
        self.portlock[type].release()
