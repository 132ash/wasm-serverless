FROM ubuntu_base

WORKDIR /app

COPY httplib.h /app/
COPY server.cpp /app/

# 暴露5000端口
EXPOSE 5000

# 留给子镜像一个入口点脚本来完成编译和启动服务器
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]