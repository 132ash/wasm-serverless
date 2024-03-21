import time

def main():
    start = time.time()
    res = arg1 + arg2
    end = time.time()
    return {'res':res, "exec_latency": end - start}
