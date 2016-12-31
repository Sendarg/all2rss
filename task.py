# coding: utf-8

import tornado.gen
import tornado.httpclient

from configs import PUB_CACHE_URL_WX, PUB_CACHE_URL, TIMEOUT, _HEADERS
from db.wx_id import manage_WX_ID


@tornado.gen.coroutine
def sync_rss_feeds():
	client = tornado.httpclient.AsyncHTTPClient()
	for key in manage_WX_ID().list_WX_KEYS():
		# todo:目前数据库只存储微信,其它站点暂时不处理
		if key.startswith("wx__"):
			url = PUB_CACHE_URL_WX.format(id=key[4:])
		else:
			url = PUB_CACHE_URL.format(key=key)
		request = tornado.httpclient.HTTPRequest(url=url,
		                                         headers=_HEADERS,
		                                         connect_timeout=TIMEOUT,
		                                         request_timeout=TIMEOUT
		                                         )
		requests = yield client.fetch(request)
		if requests:
			print "++++ Synced feeds:\t%s" % url
		else:
			print "---- Sync Failed:\t%s" % url


# sync all feed history to db
@tornado.gen.coroutine
def sync_feeds_history(history=50):
	pass
