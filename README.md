# 说明
## 目的

本程序目的是为了订阅wx订阅号,从手机端转移到rss feed的xml格式,从而可以在任意位置用任何rss订阅的客户端进行阅读,极大的改善了用户体验.

开发基于tornado,Jinja2,redis.


## 部署安装
### 1、安装依赖库
	sudo pip install requirements.txt
### 2、安装redis
#### 	根据官网文档下载安装数据库服务器软件<http://redis.io/download>
#### 	MAC上使用[brew](http://brew.sh/index_zh-cn.html)安装
		brew install redis

## 运行
### 1、根据自己需求进行配置
	配置文件: configs.py
### 2、开启redis服务器
	redis-server
### 3、进入diy目录,运行WEB项目
	python start.py


## 其它
### 1、自动化脚本运行
	nohup redis-server >/dev/null 2>&1 &
	cd  YourDirectory/all2rss/diy
	python start.py >/dev/null 2>&1 &

### 2、首次部署可删除feed_history.txt文件，以加载10页内容