#!/bin/bash

# 从DockerHub Pull下MySQL官方镜像
# 如果网速较慢，可以借助shadowsocks+proxychains4翻墙工具下载
# 具体教程可以自行搜索。
docker pull mysql:latest

# 启动MySQL容器，转发本地端口3306至容器
docker run --name local-mysql -p 0.0.0.0:3306:3306 -d \
        -e MYSQL_ROOT_PASSWORD='localdev' \
        -e MYSQL_DATABASE='poseidon' mysql

# 查看本地端口
lsof -i :3306
