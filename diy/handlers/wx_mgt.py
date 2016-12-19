# coding:utf-8

import tornado.web
from configs import WEIXIN_SOUGOU, WEIXIN_GS_ADD_URL,CACHE_URL_WX
from utils.js_helper import js_alert_j_new
from urllib import quote_plus
from utils.iHttpLib import get_GS
from urlparse import urlparse
import json

from db.wx_data_lib import wx_info as WXIF
from db.wx_id import manage_WX_ID


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		manage_WX_ID().update_WX_ID()
		list = manage_WX_ID().list_WX_ID()
		self.render('wx_mgt.html', list=list, SouGou_URL=WEIXIN_SOUGOU,RSS_URL=CACHE_URL_WX)


class DelHandler(tornado.web.RequestHandler):
	def post(self):
		self.wxid = self.request.arguments['wxid'][0]
		if not manage_WX_ID().del_WX_ID(self.wxid):
			self.write(js_alert_j_new("删除失败!!!:%s" % self.wxid))
		else:
			self.redirect("/wx_mgt")


class AddHandler(tornado.web.RequestHandler):
	def post(self):
		wx_url = self.get_argument('wx_url')
		if urlparse(wx_url)[1] != 'mp.weixin.qq.com':
			self.write(js_alert_j_new('地址错误!'))
		else:
			id_info = WXIF().get_id_info_by_url(wx_url)
			if id_info:
				gs_add_url = WEIXIN_GS_ADD_URL.format(url=quote_plus(wx_url))
				rj = json.loads(get_GS(gs_add_url))
				if rj.has_key('error'):
					if manage_WX_ID().create_WX_ID(id_info):
						alert = "++++ Added: %s:%s" % (id_info['wx_id'], id_info['name'])
						self.write(js_alert_j_new(alert))
						alert_details = alert + "\n" + json.dumps(id_info, ensure_ascii=False)
						print alert_details
					else:
						alert = "---- Maybe Already Exist: %s:%s" % (id_info['wx_id'], id_info['name'])
						self.write(js_alert_j_new(alert))
						print alert
				else:
					alert = "---- GSData 添加失败!"
					print alert
					self.write(js_alert_j_new(alert))
			else:
				alert = "---- 搜狗失败!"
				print alert
				self.write(js_alert_j_new(alert))
