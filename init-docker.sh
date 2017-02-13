#!/bin/bash
docker pull mysql:latest
docker run --name local-mysql -p 0.0.0.0:3306:3306 -d \
        -e MYSQL_ROOT_PASSWORD='localdev' \
        -e MYSQL_DATABASE='poseidon' mysql
lsof -i :3306
