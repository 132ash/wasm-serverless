import psutil
import time

def monitor_process_memory(pid):
    try:
        # 根据PID获取Process对象
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
        return

    print(f"Monitoring memory usage for PID {pid} and its children...")
    
    try:
        while True:
            # 获取主进程的内存使用信息
            main_memory_info = process.memory_info()
            print(f"Main Process: PID {pid}, RSS {main_memory_info.rss/ (1024 * 1024)}, VMS {main_memory_info.vms/ (1024 * 1024)}")

            # 遍历所有子进程，并打印它们的内存使用情况
            for child in process.children(recursive=True):
                child_memory_info = child.memory_info()
                print(f"Child Process: PID {child.pid}, RSS {child_memory_info.rss/ (1024 * 1024)}, VMS {child_memory_info.vms/ (1024 * 1024)}")
            
            # 每5秒刷新一次数据
            time.sleep(0.1)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print(f"Process with PID {pid} has terminated or access denied.")

if __name__ == "__main__":
    # 将这里的1234替换为你的C++ HTTP server的PID
    monitor_process_memory(28922)
