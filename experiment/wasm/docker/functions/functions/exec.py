import os

default_file = 'main.py'
work_dir = '/home/ash/wasm/wasm-serverless/experiment/wasm/docker/functions/pythoncode'

ctx = {'arg1':2, "arg2":3}
filename = os.path.join(work_dir, default_file)
with open(filename, 'r') as f:
    code = compile(f.read(), filename, mode='exec')


# pre-exec
exec(code, ctx)
# run function

out = eval('main()', ctx)
print(f"out: {out}")

