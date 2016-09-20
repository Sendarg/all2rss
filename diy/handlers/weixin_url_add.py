# coding:utf-8

import json
from urllib import quote_plus

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_GS_ADD_URL, GS_ADD_HEADERS, CACHE_URL_WX
from db.wx_info import get_info_by_url


class WeixinAddHandler(tornado.web.RequestHandler):
	client = tornado.httpclient.HTTPClient()

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):

		wx_url = self.request.uri[20:]
		gs_add_url = WEIXIN_GS_ADD_URL.format(url=quote_plus(wx_url))

		request = tornado.httpclient.HTTPRequest(url=gs_add_url, headers=GS_ADD_HEADERS)
		r = self.client.fetch(request).body.decode('utf-8').strip()
		rj = json.loads(r)
		if rj['error'] == 1:
			wx_info = get_info_by_url(wx_url)
			alert = "++++\tAdded:\t%s\n" % (wx_info['id'] + ":" + wx_info['name'])
			self.write(alert)
			self.write(json.dumps(wx_info, ensure_ascii=False))
			feed_url = CACHE_URL_WX.format(wx_id=wx_info['id'])
			self.write("\n++++\tRSS Feed URL:\t%s\n" % (feed_url))
		else:
			self.write("error")