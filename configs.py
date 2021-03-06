# coding:utf-8

WEIBO_URL = 'http://service.weibo.com/widget/widget_blog.php?uid={uid}'
WEIBO_LINK = 'http://weibo.com/u/{uid}'

ZHIHU_URL = 'http://news.at.zhihu.com/api/1.2/news/latest'
ZHIHU_HEAD = {'User-Agent': "ZhihuNotMoe/2333", }

# Old Sougou
# WEIXIN_KEY = 'http://weixin.sogou.com/gzh?openid={id}'
# WEIXIN_COOKIE = 'http://weixin.sogou.com/weixin?query={q}'
# WEIXIN_URL = 'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid={id}&eqs={eqs}&ekv={ekv}&page=1&t={t}'

# new Sougou
WEIXIN_KEY = 'http://weixin.sogou.com/weixin?type=1&query={id}&ie=utf8&_sug_=y&_sug_type_='
WEIXIN_SOUGOU = 'http://weixin.sogou.com/weixin?type=1&query={id}&ie=utf8&_sug_=y&_sug_type_='
WEIXIN_COOKIE = ''

# use gsdata
WEIXIN_GS_Article_URL = 'http://www.gsdata.cn/Query/article?q={id}&post_time=0&sort=-1&date=&search_field=4'
WEIXIN_GS_Name_URL = 'http://www.gsdata.cn/query/wx?q={name}'
WEIXIN_GS_Article_URL_PAGE = 'http://www.gsdata.cn/Query/article?q={id}&post_time=0&sort=-1&date=&search_field=4&page={page}'

# http://www.gsdata.cn/query/article?q=iknow021&search_field=4&post_time=0&sort=-1&read_num=0&page=3
WEIXIN_GS_COVER_URL = 'http://img1.gsdata.cn/index.php/rank/getImageUrl?callback=&hash={hash}&_='  # remove only , image not clear enough
# Page to cache at first time # only sync 5
# All history page will store by single sub process
# store max 50 is good no large 599
WEIXIN_PAGE_COUNT = 10

# add url
WEIXIN_GS_ADD_URL = 'http://www.gsdata.cn/indexGsdata/wxUrlAdd?gid=45623&content={url}'
GS_Session_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie': '7299d75074d00968e78c687fc7b5317c=91b252beadf8ceb38bf37948849ee2df803b8c3fa%3A4%3A%7Bi%3A0%3Bs%3A5%3A%2234063%22%3Bi%3A1%3Bs%3A20%3A%22test320o%40hotmail.com%22%3Bi%3A2%3Bi%3A604800%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D',
	'Connection': 'close'}

#
WXID_QUERY_URL = "http://weixin.sogou.com/weixin?type=1&query={wx_id}&ie=utf8&"

# alibaba
JAQ_URL = 'http://jaq.alibaba.com/community/category?spm=&catid={catid}'
JAQ_ARTICLE = 'http://jaq.alibaba.com/community/art/show?spm=&articleid={articleid}'

# pediy
PEDIY_URL = 'http://bbs.pediy.com/forumdisplay.php?f={fid}'

_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'close'}
TIMEOUT = 600.0

'''
预处理从缓存DB中获取html,如果能拿到,直接返回
缓存DB的结果都有过期时间,过期后则再次爬去最新的内容
'''
ZHIHU_EXPIRES = 4 * 60 * 60  # 知乎日报内容缓存3小时
WEIXIN_EXPIRES = 5 * 60 * 60  # 微信公众号内容缓存3小时
JAQ_EXPIRES = 24 * 60 * 60  # 阿里聚安全内容缓存3小时
PEDIY_EXPIRES = 4 * 60 * 60  # 缓存3小时 http://bbs.pediy.com/forumdisplay.php?f=161

import os

# server
Server_IP = '127.0.0.1'
# Server_IP = '0.0.0.0'
PORT = '2102'
BASE_URL = 'http://%s:%s' % (Server_IP, PORT)

PUB_IP = '180.169.101.117'
PUB_NAT_IP = '172.31.16.20'
# Feeds
# PUB_CACHE_URL_WX = 'http://%s:%s/weixin?id={id}' % (PUB_IP, PUB_PORT)
PUB_CACHE_URL_WX = 'http://%s:%s/weixin?id={id}' % (Server_IP, PORT)
PUB_CACHE_URL = 'http://%s:%s/{key}' % (Server_IP, PORT)
CACHE_PERIODIC = 25 * 60 * 1000 # 65min
# CACHE_PERIODIC = ((4 * 60) + 5 )* 60 * 1000  # sync every 4 hours 5min


from  redis import Redis

# many redis can listen to 1 port,so you need kill
redisDB = Redis(password="vr2MD#a886d")
# redisDB = Redis(host='rss-redis', password="vr2MD#a886d") # use in docker bridge network


neo4j_Host = "localhost:7474"
from py2neo import Graph, authenticate


class neo4j():
	def neo4j(self):
		# set up authentication parameters
		authenticate(neo4j_Host, "neo4j", "neo4321")
		neo4j=Graph("http://%s/db/data/"%neo4j_Host)
		# neo4j=Graph(host='rss-neo4j',user='neo4j', password='neo4321')
		return neo4j
