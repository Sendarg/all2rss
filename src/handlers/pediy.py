# coding:utf-8

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import PEDIY_URL

from base import pediyBaseHandler
from utils.jaq import process_list, process_content


class pediyHandler(pediyBaseHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		client = tornado.httpclient.AsyncHTTPClient()
		client.configure(None, max_clients=100)



		id = self.key[7:]
		link = PEDIY_URL.format(fid=id)

		# 获取title


		# 获取文章列表,同步逐个获取
		items = []



		# TODO:后面一步步解析,主要参考微信操作

