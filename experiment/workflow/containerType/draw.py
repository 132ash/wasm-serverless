import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
file_path = '/home/ash/wasm/wasm-serverless/experiment/result/containerType/workflow_result.csv'
data = pd.read_csv(file_path)

mean_delay = data.groupby('container').mean()
std_delay = data.groupby('container').std()

plt.rcParams.update({'font.size': 40, 'errorbar.capsize': 200})

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))


ax2 = ax1.twinx()
ax1.set_xlabel('Start Mode')
ax1.set_ylabel('Cold Start Latency', color='tab:red')
ax2.set_ylabel('Warm Start Latency', color='tab:blue')

# Set positions and width for the bars
positions = np.arange(len(mean_delay.index))
width = 0.35

# Plotting Cold Startup Latency
cold_bars = ax1.bar(positions - width/2, mean_delay['cold'], width, yerr=std_delay['cold'], color='tab:red', label='Cold', capsize=5)
# Plotting Warm Startup Latency
warm_bars = ax2.bar(positions + width/2, mean_delay['warm'], width, yerr=std_delay['warm'], color='tab:blue', label='Warm', capsize=5)

ax1.set_title('End to end latency by container type and start mode.')
ax1.set_xticks(positions)
ax1.set_xticklabels(mean_delay.index)

ax1.tick_params(axis='y', labelcolor='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:blue')

fig.tight_layout()

plt.show()
