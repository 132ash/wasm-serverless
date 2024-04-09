import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

file_path = "/home/ash/wasm/wasm-serverless/experiment/result/groupingCost.csv"
data = pd.read_csv(file_path)

plt.rcParams.update({'font.size': 40,})

# Plotting
fig, ax1 = plt.subplots()


ax2 = ax1.twinx()
ax1.plot(data['node'], data['core x second'], 'g-', label='CPU Usage (core x second)',linewidth =4.0)
ax2.plot(data['node'], data['mem_usage'], 'b-', label='Memory Usage (MB)',linewidth =4.0)

ax1.set_xlabel('Number of Nodes')
ax1.set_ylabel('CPU Usage (core x second)', color='g')
ax2.set_ylabel('Memory Usage (MB)', color='b')

ax1.tick_params(axis='y', labelcolor='g')
ax2.tick_params(axis='y', labelcolor='b')

# Adding a legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.title('CPU and Memory Usage by Node Count')
plt.show()