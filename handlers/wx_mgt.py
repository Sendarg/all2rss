# coding:utf-8

import tornado.web
from configs import WEIXIN_SOUGOU, WEIXIN_GS_ADD_URL, PUB_CACHE_URL_WX, WEIXIN_GS_Name_URL, WEIXIN_GS_Article_URL
from utils.js_helper import js_alert_refresh
from urllib import quote_plus
from utils.iHttpLib import get1_GS
from urlparse import urlparse
import json

from db.wx_data_lib import wx_info as WXIF
from db.wx_id import manage_WX_ID
import socket


class MainHandler(tornado.web.RequestHandler):
	def verifyLocalhost(self):
		hostname = socket.getfqdn(socket.gethostname())
		hostIP = socket.gethostbyname(hostname)
		if self.request.remote_ip != hostIP:
			return hostIP
		else:
			return "Pass"
	
	def get(self):
		# if  random.randint(0,4)== 0:# only 1/3的可能会更新
		# if self.verifyLocalhost():
		list = manage_WX_ID().list_WX_ID()
		group = manage_WX_ID().list_Groups()
		self.render('wx_mgt.html',
		            list=list,
		            group=group,
		            GSdata_URL=WEIXIN_GS_Name_URL,
		            SouGou_URL=WEIXIN_SOUGOU,
		            GSdata_List_URL=WEIXIN_GS_Article_URL,
		            RSS_URL=PUB_CACHE_URL_WX)
	
	def prepare(self):
		# todo: can't use host need some auth like basic
		pass
		
		# verifyIP = MainHandler.verifyLocalhost(self)
		# if verifyIP != "Pass":
		# 	# self.write("Not Allowed:\t%s" % verifyIP)
		# 	# self.finish()


class UpdateHandler(MainHandler):
	def post(self):
		manage_WX_ID().update_WX_ID()
		self.redirect("/wx_mgt")


class GroupHandler(MainHandler):
	def post(self):
		self.group = self.request.arguments['group'][0]
		self.wx_id = self.request.arguments['wx_id'][0]
		if not manage_WX_ID().set_Group(self.wx_id, self.group):
			self.write(js_alert_refresh("设置分组失败!!!\nID:%s\nGroup:%s" % (self.wx_id, self.group)))
		else:
			self.redirect("/wx_mgt")


class ImportHandler(MainHandler):
	def post(self):
		self.fileinfo = self.request.files['file'][0]
		if not manage_WX_ID().mass_Import_WX_ID_from_opml(self.fileinfo['body']):
			info = "批量导入Feeds失败!!!opmlFile:%s" % (self.fileinfo['filename'])
			print info
			self.write(js_alert_refresh(info))
		else:
			info = "==== Import RSS Feeds Success! opmlFile:%s" % (self.fileinfo['filename'])
			print info
			self.write(js_alert_refresh(info))


class FeedsHandler(MainHandler):
	def post(self):
		if self.request.arguments.has_key("group"):
			self.group = self.request.arguments['group'][0]
		else:
			self.group = ""
		
		feeds = manage_WX_ID().export_Feeds(self.group)
		print "==== Render RSS Feeds Success! Group:\t%s" % self.group
		self.set_header("Content-Type", "application/opml+xml")
		self.render("feeds.opml",
		            feeds=feeds,
		            CACHE_URL_WX=PUB_CACHE_URL_WX)
		# self.write(js_alert_refresh("获取Feeds失败!!!Group:%s" % (self.group)))
			
		
	get=post # You still need get if you want access the page, because access the page using browser request with GET method.

class DelHandler(MainHandler):
	def post(self):
		self.wxid = self.request.arguments['wxid'][0]
		if not manage_WX_ID().del_WX_ID(self.wxid):
			self.write(js_alert_refresh("删除失败!!!:%s" % self.wxid))
		else:
			self.redirect("/wx_mgt")


class AddHandler(MainHandler):
	def post(self):
		wx_url = self.get_argument('wx_url')
		if urlparse(wx_url)[1] != 'mp.weixin.qq.com':
			self.write(js_alert_refresh('地址错误!'))
		else:
			id_info = WXIF().get_id_info_by_url(wx_url)
			if id_info:
				gs_add_url = WEIXIN_GS_ADD_URL.format(url=quote_plus(wx_url))
				rj = json.loads(get1_GS(gs_add_url))
				if rj.has_key('error'):
					if manage_WX_ID().create_WX_ID(id_info):
						alert = "++++ Added! ^_^\t%s\t%s" % (id_info['wx_id'], id_info['name'])
						self.write(js_alert_refresh(alert))
						alert_details = alert + "\n" + json.dumps(id_info, ensure_ascii=False)
						print alert_details
					else:
						alert = "---- Maybe Already Exist!!!\t%s\t%s" % (id_info['wx_id'], id_info['name'])
						self.write(js_alert_refresh(alert))
						print alert
				else:
					alert = "---- GSData 添加失败!"
					print alert
					self.write(js_alert_refresh(alert))
			else:
				alert = "---- 搜狗失败!"
				print alert
				self.write(js_alert_refresh(alert))
