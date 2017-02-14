#!/bin/bash

PREFIX=$(cd `dirname $0`; pwd)
docker pull mysql:5.7.17
docker run --name local-mysql-dev -p 0.0.0.0:3306:3306 -d \
        -v ${PREFIX}:/etc/mysql/conf.d \
        -e MYSQL_ROOT_PASSWORD='localdevmanager' \
        -e MYSQL_USER='dev' \
        -e MYSQL_PASSWORD='jkL8jDequ0IcTTeZ' \
        -e MYSQL_DATABASE='poseidon' mysql
lsof -i :3306
