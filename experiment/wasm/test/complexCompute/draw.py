import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import yaml
sys.path.append("/home/ash/wasm/wasm-serverless/experiment")
import config
import requests

resdir = config.RESULT_DIR

# 去除未命名的索引列

# 假设 data 是通过 pd.read_csv('/path/to/your/data_transfer(ms).csv') 读取的DataFrame
# 这里是从CSV文件中读取数据的代码示例
funcNames = ['spectral_norm', 'binarytree']
filePath = {func:'/'.join([resdir,"complexCompute",f'{func}_performance_py.csv']) for func in funcNames}
param_list = {
               'spectral_norm':[10 * i for i in range(1,21)],
               'binarytree': [i for i in range(1,11)]
            }

data_dict = {}
for func in funcNames:
    data_dict[func] = pd.read_csv(filePath[func])

mode  = sys.argv[1]
if mode == "double":
    for func, platforms in data_dict.items():
            plt.rcParams.update({'font.size': 25})
            plt.figure(figsize=(10, 6))
            plt.title(f'Performance Comparison: {func}')

            plt.tick_params(labelsize=23)
            
            # 绘制WASM性能曲线
            ax1 = plt.gca()  # 获取当前轴
            ax1.plot(param_list[func], platforms['WASM'], 'r-', label='WASM', linewidth =4.0)
            ax1.set_xlabel('Input Size')
            ax1.set_ylabel('WASM Time (s)', color='r',fontsize=25)
            ax1.tick_params(axis='y', labelcolor='r',labelsize=25)
            
            # 绘制Docker性能曲线
            ax2 = ax1.twinx()  # 共享x轴的第二个y轴
            ax2.plot(param_list[func], platforms['Docker'], 'b-', label='Docker', linewidth =4.0)
            ax2.set_ylabel('Docker Time (s)', color='b',fontsize=25)
            ax2.tick_params(axis='y', labelcolor='b',labelsize=25)
            
            # 图例
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc='upper left')
            
            plt.show()
else:
    for func, platforms in data_dict.items():
        plt.rcParams.update({'font.size': 25})
        plt.figure(figsize=(10, 6))
        plt.title(f'Performance Comparison: {func}')
        
        plt.tick_params(labelsize=23)
        
        # 绘制WASM性能曲线
        plt.plot(param_list[func], platforms['WASM'], 'r-', label='WASM', linewidth=4.0)
        
        # 绘制Docker性能曲线
        plt.plot(param_list[func], platforms['Docker'], 'b-', label='Docker', linewidth=4.0)
        
        plt.xlabel('Input Size', fontsize=25)
        plt.ylabel('Time (s)', fontsize=25)
        plt.tick_params(axis='y', labelsize=25)
        
        # 图例
        plt.legend(loc='upper left', fontsize=20)
        
        plt.show()
