# 说明
## 目的

本程序目的是为了订阅wx订阅号,从手机端转移到rss feed的xml格式,从而可以在任意位置用任何rss订阅的客户端进行阅读,极大的改善了用户体验.

## 技术说明
开发基于tornado Jinja2 redis.

性能方面:通过异步获取相关内容源存储到redis缓存,来提供高性能访问和读取.

内容方面:提供原生的阅读体验,如封面图片展现,内容样式处理,原始链接访问.

当前受限:目前大部分订阅支持,某小众内容暂未收录.

默认配置设计:首次部署可删除feed_history.txt文件,以加载10页内容,二次访问仅加载最新一页内容.



## 部署安装
### 1、安装依赖库
	sudo pip install -r requirements.txt
### 2、安装redis
根据官网文档下载安装Redis服务器:<http://redis.io/download>

For NoWindows:<http://redis.io/download>

For Windows:<https://github.com/MSOpenTech/redis/releases>

MAC上使用[brew](http://brew.sh/index_zh-cn.html)安装

	brew install redis

## 运行
### 1、根据自己需求进行配置
	配置文件: configs.py
### 2、开启redis服务器
	redis-server
### 3、进入diy目录,运行WEB项目
	python start.py

## 使用1-有订阅内容
### 1、打开本地server,或你配置的公网server(建议)
默认配置<http://127.0.0.1:2102/>
### 2、搜索需要订阅的wx号[功能不完善,暂时无效]
### 3、直接访问服务器地址来获取内容
如笑来的学习订阅号:<http://127.0.0.1:2102/weixin?id=xiaolai-xuexi>

## 使用2-无订阅返回,需要手动添加新收录URL,第二天生效
新增URL<http://127.0.0.1:2102/weixin_url_add?url=/>


## 客户端订阅
### 把上面的地址导入到你的rss客户端


## 后台服务运行,服务器或本地自动化脚本
	nohup redis-server >/dev/null 2>&1 &
	cd  YourDirectory/all2rss/diy
	python start.py >/dev/null 2>&1 &