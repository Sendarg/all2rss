# coding:utf-8

import json
from urllib import quote_plus

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_GS_ADD_URL, CACHE_URL_WX
import db.wx_data_lib
from utils.iHttpLib import get_GS

'''
No longer Needed,Do it in wx_mgt.py
'''
class WeixinAddHandler(tornado.web.RequestHandler):

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		wx_url = self.request.uri[20:]
		gs_add_url = WEIXIN_GS_ADD_URL.format(url=quote_plus(wx_url))
		rj = json.loads(get_GS(gs_add_url))
		if rj['error'] == 1:
			wx_info = db.wx_data_lib.wx_info().get_info_by_url(wx_url)
			if wx_info:
				alert = "++++\tAdded:\t%s\n" % (wx_info['wx_id'] + ":" + wx_info['name'])
				self.write(alert)
				self.write(json.dumps(wx_info, ensure_ascii=False))
				feed_url = CACHE_URL_WX.format(id=wx_info['wx_id'])
				self.write("\n++++\tRSS Feed URL:\t%s\n" % (feed_url))
			else:
				alert = "----\tError URL:\t%s\n" % (wx_url)
				self.write(alert)
		else:
			self.write("error")