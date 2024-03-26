import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 去除未命名的索引列

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
file_path = '/home/ash/wasm/wasm-serverless/experiment/result/coldstart(ms).csv'
data = pd.read_csv(file_path)
data_coldstart_cleaned = data.drop(columns=['Unnamed: 0'])

# 计算平均值和标准差
mean_coldstart = data_coldstart_cleaned.mean()
std_coldstart = data_coldstart_cleaned.std()

# 设置柱状图的位置和宽度
ind = np.arange(len(mean_coldstart))
width = 0.35

fig, ax = plt.subplots()

# 绘制柱状图
coldstart_bars = ax.bar(ind, mean_coldstart, width, yerr=std_coldstart, capsize=5)

# 添加一些文本用于标签、标题和自定义x轴刻度等
ax.set_ylabel('Cold Start Time (ms)')
ax.set_title('Cold Start Time by Platform')
ax.set_xticks(ind)
ax.set_xticklabels(mean_coldstart.index)
ax.legend(coldstart_bars, mean_coldstart.index)

fig.tight_layout()

plt.show()
