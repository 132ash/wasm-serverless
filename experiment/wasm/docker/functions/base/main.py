import time
import string
import random

def main():
    start = time.time()
    time.sleep(2)
    end = time.time()
    return {'res': 1, 'latency':end - start}
