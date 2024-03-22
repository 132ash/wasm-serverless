#!/bin/bash

# 编译服务器和提供的mainFunction实现
g++ -std=c++11 -O3 /app/server.cpp /app/mainFunction.cpp -o /app/server -ljsoncpp -pthread

# 启动服务器
/app/server