## 爬取知乎专题的爬虫

### 一、初衷

### 爬取知乎，精华问题，与精华回答。

## 二、初始化

### 1、安装docker
```shell
./init-docker.sh
```

### 2、安装Python依赖
```shel
pip install -r requirements.txt -i http://pypi.doubanio.com/simple --trusted-host pypi.doubanio.com
```

### 3、初始化数据库
```shell
python db.py
```
