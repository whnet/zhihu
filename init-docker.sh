#!/bin/bash

# 从DockerHub Pull下MySQL官方镜像
docker pull mysql:latest

# 启动MySQL容器，转发本地端口3306至容器
docker run --name local-mysql -p 0.0.0.0:3306:3306 -d \
        -e MYSQL_ROOT_PASSWORD='localdev' \
        -e MYSQL_DATABASE='poseidon' mysql

# 查看本地端口
lsof -i :3306
