import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
file_path = '/home/ash/wasm/wasm-serverless/experiment/result/data_transfer(ms).csv'
data = pd.read_csv(file_path)

# 计算每个平台和每种数据大小的平均传输时延和标准差
mean_delay = data.groupby('Source').mean()
std_delay = data.groupby('Source').std()

# 数据大小标签
data_sizes = mean_delay.columns

# 位置索引和宽度
ind = np.arange(len(data_sizes))  # x轴上的位置索引
width = 0.35  # 柱状图的宽度
plt.rcParams.update({'font.size': 25, 'errorbar.capsize': 200})

# 重新绘制柱状图，这次带有更大的字体和更粗的误差线
fig, ax = plt.subplots(figsize=(10, 6)) 

# 绘制wasm平台的柱状图
wasm_bars = ax.bar(ind - width/2, mean_delay.loc['wasm'], width, yerr=std_delay.loc['wasm'],
                   label='WASM', capsize=5)

# 绘制docker平台的柱状图
docker_bars = ax.bar(ind + width/2, mean_delay.loc['docker'], width, yerr=std_delay.loc['docker'],
                     label='Docker', capsize=5)
ax.set_yscale('log')
ax.set_yticks([1, 10, 100, 1000])
# 添加一些文本用于标签、标题和自定义x轴刻度等
ax.set_xlabel('Data Size')
ax.set_ylabel('Transfer Delay (ms)')
ax.set_title('Transfer Delay by Platform and Data Size')
ax.set_xticks(ind)
ax.set_xticklabels(data_sizes)
ax.legend()

# 在柱状图上方添加数值标签
def autolabel(bars):
    """Attach a text label above each bar in *bars*, displaying its height."""
    for bar in bars:
        height = bar.get_height()
        ax.annotate('%.2f' % height,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(wasm_bars)
autolabel(docker_bars)

fig.tight_layout()

plt.show()

