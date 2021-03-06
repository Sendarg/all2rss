# coding:utf-8
import tornado.gen
from utils.iHttpLib import getAClient,reqsBuilder
import tornado.web
from tornado.web import HTTPError
from configs import WEIXIN_GS_Article_URL, WEIXIN_GS_Article_URL_PAGE,GS_Session_HEADERS

from base import WeixinBaseHandler
from db.wx_data_lib import wx_info
from db.wx_msg import storeMsg
from db.wx_id import manage_WX_ID
import re,json




class WeixinHandler(WeixinBaseHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		id = self.key[4:]
		link = WEIXIN_GS_Article_URL.format(id=id)

		# 确认ID和存储ID
		# 如果获取不到准确的ID信息,账号已不存在,取消全部操作
		# 如果获得的到,存储到db,下面不再每次存储

		if manage_WX_ID().check_ID(id):

			# 访问api url,获取公众号文章列表\基本信息,同步逐个获取
			msg_data_all = []
			## method 1 ,long
			# for p in range(self.page_size):# 读取X页结果,第一次获取5页结果,第二次获取一页结果?
			#     url = WEIXIN_URL_PAGE.format(id=id,page=p)  # 生成api url
			#     print "++++	Processing WeiXin\t[%s]++++" % url
			#     request = tornado.httpclient.HTTPRequest(url=url)
			#     response =  client.fetch(request,
			#                               # raise_error=False,
			#                               connect_timeout=TIMEOUT,
			#                               request_timeout=TIMEOUT,
			#                              headers=_HEADERS
			#                               )
			#
			#     if response.code == 200:
			#         rc = response.body.decode('utf-8')
			#         [items.append(i) for i in process_list(rc)]# 解析文章列表
			#     else:
			#         print "----	Faile URL\t[%s] ----" % url

			## another method to write
			print "====	Processing WeiXin\t[%s&pageCount=%d]++++" % (link, self.page_count)

			urls=[WEIXIN_GS_Article_URL_PAGE.format(id=id, page=p + 1) for p in range(self.page_count)]
			# todo: NOW GS page need login session
			client_gs=getAClient(max_clients=100)
			listResponses=yield [client_gs.fetch(r) for r in reqsBuilder(urls,_HEADERS=GS_Session_HEADERS)]
			
			# ## for catch except
			# def gs_fetch(urls):
			# 	for r in reqsBuilder(urls, _HEADERS=GS_Session_HEADERS):
			# 		try:
			# 			response = client_gs.fetch(r)
			# 		except HTTPError:
			# 			print "---- Tornado HTTPError:\t%s" % r
			# 			response = None
			# 		yield response
			#
			# listResponses = gs_fetch(urls=urls)
			

			for p, response in enumerate(listResponses):
				gs_url = response.request.url
				# gs_url = WEIXIN_GS_URL_PAGE.format(id=id, page=p + 1)
				# local_url = '%s&page=%d' % (self.url, p + 1) # not useful
				if response.code == 200:
					rc = response.body.decode('utf-8')
					# msg_urls = re.findall(r"'url':'(\S+)'", rc)
					'''
					data="{'url':'http://mp.weixin.qq.com/s?__biz=MzA5NzQ3NDA2OA==&mid=2457549036&idx=1&sn=8742f93466f5c6ef183622ead6e634a9&chksm=872fdb97b05852812f85d0f8f8688b80cb5180919539012c39492f15720e4666631ced0ec466&scene=4#wechat_redirect','pic':'aHR0cDovL21tYml6LnFwaWMuY24vbW1iaXpfanBnL3BRRjRjend6MHpPVnhvS2ljdjB6V09mUWlhZjB6azJ5SmJCcFBHbGljWDVpYnFXRW1ZaWMxVDRQa3QxalhzV0l2aWFpY1BPMkFOSU9pYnBxMm1ZVkNUWkVTaWJiaWNpYkEvMD93eF9mbXQ9anBlZ3w1NDQ5MTlhZjE3YWUwZWU5MjRjNzY2ZmZmMzNjZTA4Ng==','text':'以“用户为中心”的画布工具是什么?怎么用?价值在哪？'}">
					'''
					msg_data = re.findall(r'data="(\{.*\})">', rc)
					msg_data_all.extend(msg_data)
					print "====	Success URL\t[%s] ----" % gs_url

				else:
					print "----	Faile URL\t[%s] ----" % gs_url
					
			# 访问微信信息url,获取全部内容
			items = []
			if msg_data_all :  #  and len(msg_data_all) > 5 随机抽取校验是否合法结果
				# 获取每一个文章的封面
				# for xinshengdaxue on openshift Code 500? ???
				# TODO error in feed,no reach store step
				'''
				wx__bj-jusfoun
				wx__duzhe3650

				File "/Users/neoo/PycharmProjects/all2rss/diy/handlers/weixin_gs.py", line 88, in get
				r=response.body.decode('utf-8').strip()

				raise_exc_info(self._exc_info)
				  File "<string>", line 3, in raise_exc_info
				HTTPError: HTTP 500: Internal Server Error
				ERROR:tornado.access:500 GET /weixin?id=bj-jusfoun (127.0.0.1) 7028.01ms

				'''
				'''
				# small cover img
				coverResponses =  yield [clientAsync.fetch(WEIXIN_GS_COVER_URL.format(hash=i['msg_img']))
										 for i in items]
				for i, response in enumerate(coverResponses):
					coverurl = ''
					if response.code == 200 and '":"' in response.body.decode('utf-8'):

						#raise ValueError("No JSON object could be decoded")
						#   ValueError: No JSON object could be decoded

						r=response.body.decode('utf-8').strip()
						try:
							rc = json.loads(r)
						except ValueError:
							print "---- Retry:\t%s ----"%self.url
							yield clientAsync.fetch(self.url)# request again

						if rc and dict(rc).has_key('url'):
							coverurl = rc['url']
					items[i]['msg_cover']=coverurl
				'''
				# 爬取每篇文章的内容
				client_wx = getAClient(max_clients=400)
				
				## get URL from metadata[url、pic、text]
				msg_data_json=[]
				for msg in msg_data_all:
					out=msg.replace("\"", "\\\"").replace("'", "\"") #  when replace to  " first care exits "
					try:
						out=json.loads(out)
						msg_data_json.append(out)
					except ValueError as e:
						print "---- JSON ERROR:\t%s\n%s\n%s"%(e.message,msg,out)
					
				msg_url_all=[msg["url"] for msg in msg_data_json]
				responses = yield [client_wx.fetch(u) for u in reqsBuilder(msg_url_all)]
				# warn_count = 0  # 排除删除的文章
				for i, response in enumerate(responses):
					if response.code == 200:
						html = response.body.decode('utf-8')

						# build content may be empty:
						if "icon_msg warn" in html:
							print "----\t[ %s ]\t内容已被删除或屏蔽" % id
							# warn_count += 1
							continue  # skip one

						# 合并3个字典 http://codingpy.com/article/the-idiomatic-way-to-merge-dicts-in-python/
						# 后面的覆盖前面的字段
						# 因为信息可能重复,暂且不管process_list输出的重复信息
						full_info = wx_info().get_full_info_by_html(html)
						# 存储到数据库和数组
						if storeMsg().create_WX_MSG_FULL(full_info):
							items.append(full_info)
							# print LED
							print "++++\tGet items\t++++"
							print full_info['wx_id']+"\t"+full_info['name']
							print full_info['msg_createdtime']
							print full_info['msg_title']
							print full_info['msg_desc']
							print full_info['msg_link']
							print "_____________________ single msg split\t%s\t_____________________" % str(i + 1)


				'''
				# todo error
				File "/Users/neoo/PycharmProjects/all2rss/diy/handlers/weixin_gs.py", line 120, in get
				else:
				AttributeError: 'str' object has no attribute 'has_key'
				ERROR:tornado.access:500 GET /weixin?id=duzhe3650 (127.0.0.1) 11682.56ms

				'''
				# check item's <description><![CDATA[]]></description>
				if type(items[0]) == dict and items[0].has_key('msg_content') and items[0]['msg_content']:
					pubdate = items[0]['msg_createdtime']
					title = items[0]['name']
					description = items[0]['desc']

					self.set_header("Content-Type", "application/xml")
					self.render("rss.xml", title=title, description=description, items=items, pubdate=pubdate,
					            link=link)
				else:
					self.redirect("/")
			else:
				self.redirect("/")