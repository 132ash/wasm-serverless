import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
file_path = "C:\\Users\\27409\Desktop\graduate project\code\wasm-serverless\experiment\\result\scaleupspeed.csv"
df = pd.read_csv(file_path)  


plt.figure(figsize=(10, 6))

# 分平台绘制折线图
for platform, group_df in df.groupby('Platform'):
    plt.plot(group_df['Time'], group_df['Containers'], label=platform,linewidth =4.0)

# 添加图例
plt.rcParams.update({'font.size': 25})
plt.legend(loc='upper right')

# 添加标题和坐标轴标签
plt.title('Container Count Over Start Time by Platform')
plt.xlabel('Time', fontsize=40)
plt.ylabel('Container Count', fontsize=40)
plt.tick_params(labelsize=40)

# 显示图表
 # 显示图表
plt.show()