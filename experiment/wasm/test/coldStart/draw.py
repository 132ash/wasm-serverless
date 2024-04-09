import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 去除未命名的索引列

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
file_path = '/home/ash/wasm/wasm-serverless/experiment/result/coldstart(ms).csv'
data_coldstart_cleaned = pd.read_csv(file_path)

# 计算平均值和标准差
mean_coldstart = data_coldstart_cleaned.mean()
std_coldstart = data_coldstart_cleaned.std()

print(mean_coldstart)

# 设置柱状图的位置和宽度
ind = np.arange(len(mean_coldstart))
width = 0.35

plt.rcParams.update({'font.size': 40, 'errorbar.capsize': 200})

# 重新绘制柱状图，这次带有更大的字体和更粗的误差线
fig, ax = plt.subplots(figsize=(10, 6)) 

# 绘制柱状图
coldstart_bars = ax.bar(ind, mean_coldstart, width, yerr=std_coldstart, capsize=5)
# ax.set_yscale('log')

# # 设置刻度为1, 10, 100, 1000
# ax.set_yticks([1, 10, 100, 1000])
# 添加一些文本用于标签、标题和自定义x轴刻度等
ax.set_ylabel('Cold Start Time (ms)')
ax.set_title('Cold Start Time by Platform')
ax.set_xticks(ind)
ax.set_xticklabels(mean_coldstart.index)
ax.legend(coldstart_bars, mean_coldstart.index, loc="upper left")

fig.tight_layout()

plt.show()

