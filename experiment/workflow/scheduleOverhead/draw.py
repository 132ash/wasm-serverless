import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 去除未命名的索引列

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
workerPath = '/home/ash/wasm/wasm-serverless/experiment/result/scheduleCost_test/WorkerSP_scheduleCost.csv'
masterPath = '/home/ash/wasm/wasm-serverless/experiment/result/scheduleCost_test/MasterSP_scheduleCost.csv'
data_worker = pd.read_csv(workerPath)
data_master = pd.read_csv(masterPath)
workflows = list(data_worker.columns.values)
plt.rcParams.update({'font.size': 40, 'errorbar.capsize': 200})


# 计算平均值和标准差
mean_latency_worker = data_worker.mean()
mean_latency_master = data_master.mean()

x = np.arange(len(workflows))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, mean_latency_master, width, label='MasterSp')
rects2 = ax.bar(x + width/2, mean_latency_worker, width, label='WorkerSp')

# 绘制柱状图
ax.set_ylabel('Scheduling Overhead (seconds)')
ax.set_title('Scheduling Overhead by WOrkflow and Mode')
ax.set_xticks(x)
ax.set_xticklabels(workflows)
ax.legend()
fig.tight_layout()

plt.show()


