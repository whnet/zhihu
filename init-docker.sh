#!/bin/bash

# 从DockerHub Pull下MySQL官方镜像
# 网速较慢，可以借助shadowsocks+proxychains4翻墙工具下载
docker pull mysql:latest

docker run --name local-mysql -p 0.0.0.0:3306:3306 -d \
        -e MYSQL_ROOT_PASSWORD='localdev' \
        -e MYSQL_DATABASE='poseidon' mysql

# 查看本地端口
lsof -i :3306
