# 检查是否有一个参数被传入
if [ $# -ne 1 ]; then
    echo "Usage: $0 <TEST_TIME>"
    exit 1
fi

# 获取整型参数
INT_ARG=$1

# 设置工作目录的路径
WORKDIR="/home/ash/wasm/wasm-serverless/experiment/wasm/test"

# 遍历工作目录下的所有子目录
for dir in "$WORKDIR"/*; do
    if [ -d "$dir" ]; then # 确保是目录
        # 检查目录内是否存在main.py文件
        if [ -f "$dir/test.py" ]; then
            echo "test in $dir with testTime $INT_ARG"
            # 在子目录内执行main.py文件，传入整型参数
            python "$dir/test.py" $INT_ARG
        else
            echo "test.py not found in $dir"
        fi
    fi
done