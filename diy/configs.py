# coding:utf-8

WEIBO_URL = 'http://service.weibo.com/widget/widget_blog.php?uid={uid}'
WEIBO_LINK = 'http://weibo.com/u/{uid}'

ZHIHU_URL = 'http://news.at.zhihu.com/api/1.2/news/latest'
ZHIHU_HEAD = {'User-Agent':"ZhihuNotMoe/2333",}

# Old Sougou
# WEIXIN_KEY = 'http://weixin.sogou.com/gzh?openid={id}'
# WEIXIN_COOKIE = 'http://weixin.sogou.com/weixin?query={q}'
# WEIXIN_URL = 'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid={id}&eqs={eqs}&ekv={ekv}&page=1&t={t}'

# use gsdata
# WEIXIN_KEY = 'http://www.gsdata.cn/Query/wx?q={id}'
# WEIXIN_COOKIE = 'http://www.gsdata.cn/Query/article?q={q}'
WEIXIN_URL = 'http://www.gsdata.cn/Query/article?q={id}&post_time=0&sort=-1&date=&search_field=4'
WEIXIN_URL_PAGE = 'http://www.gsdata.cn/Query/article?q={id}&post_time=0&sort=-1&date=&search_field=4&page={page}'
WEIXIN_COVER_URL='http://img1.gsdata.cn/index.php/rank/getImageUrl?callback=&hash={hash}&_='
WEIXIN_PAGE_COUNT=10
# add url
WEIXIN_ADD_URL = 'http://www.gsdata.cn/indexGsdata/wxUrlAdd?gid=45623&content={url}'
ADD_HEADERS={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': '7299d75074d00968e78c687fc7b5317c=91b252beadf8ceb38bf37948849ee2df803b8c3fa%3A4%3A%7Bi%3A0%3Bs%3A5%3A%2234063%22%3Bi%3A1%3Bs%3A20%3A%22test320o%40hotmail.com%22%3Bi%3A2%3Bi%3A604800%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D',
    'Connection': 'close'}




JAQ_URL = 'http://jaq.alibaba.com/community/category?spm=&catid={catid}'
JAQ_ARTICLE='http://jaq.alibaba.com/community/art/show?spm=&articleid={articleid}'



_HEADERS={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close'}
TIMEOUT=300

'''
预处理从缓存DB中获取html,如果能拿到,直接返回
缓存DB的结果都有过期时间,过期后则再次爬去最新的内容
'''
ZHIHU_EXPIRES = 4*60*60 # 知乎日报内容缓存3小时
WEIXIN_EXPIRES = 6*60*60 # 微信公众号内容缓存3小时
JAQ_EXPIRES = 24*60*60 # 阿里聚安全内容缓存3小时



import os
# server
# IP = os.environ['OPENSHIFT_DIY_IP']
# PORT = int(os.environ['OPENSHIFT_DIY_PORT'])
IP = '127.0.0.1'
PORT = '2102'
BASE_URL='http://%s:%s'%(IP,PORT)


# rss list story file
_dir=os.path.abspath(os.path.dirname(__file__))
FEED_HIS_FILE=os.path.join(_dir, 'feed_history.txt')


# cache
# CACHE_URL_WX= 'http://all2rss-devox.rhcloud.com/weixin?id={wxid}'
# CACHE_URL= 'http://all2rss-devox.rhcloud.com/{key}'
CACHE_URL_WX='http://%s:%s/weixin?id={wx_id}'%(IP,PORT)
CACHE_URL='http://%s:%s/{key}'%(IP,PORT)
CACHE_PERIODIC= ((6 * 60)+5 * 60) * 1000 # sync every 4 hours 5min
