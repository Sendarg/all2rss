# coding:utf-8

from configs import WXID_QUERY_URL,_HEADERS

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

from lxml import html as Xhtml
import lxml,re
from utils.date_format import weixindate_fromTS
from html2text import unescape


class wx_info(object):
	def __init__(self):
		pass
		'''
		return wx_info dict:
		wx_info['wx_id']
		wx_info['desc']
		wx_info['name']
		wx_info['last_msg']
		wx_info['msg_book']
		wx_info['msg_up']
		wx_info['msg_date']
		wx_info['msg_createdtime']
		wx_info['msg_title']
		wx_info['msg_desc']
		wx_info['msg_cover']
		wx_info['msg_link']
		wx_info['msg_source']
		wx_info['msg_author']
		wx_info['msg_content']
		'''

	def fetch_url_g(self, url):
		# client = HTTPClient() #  _close attribute error
		# r=client.fetch(url).body.decode('utf-8').strip()
		# client.close()

		url = URL(url)

		http = HTTPClient(url.host,headers=_HEADERS)
		response = http.get(url.request_uri)
		if not response.status_code==200:
			print "----\tResponse Code[%s]\t%s" %(response.status_code, url)
			return False

		body = response.read()
		r=body.decode('utf-8').strip()
		http.close()
		return  r

	def browser_url(self,url):
		# try to anti antispider
		from selenium import webdriver
		driver = webdriver.PhantomJS()
		driver.set_window_size(1120, 550)
		driver.get(url)
		driver.refresh()
		r=driver.page_source
		print driver.current_url
		driver.quit()

		return r



	def get_id_info(self, wx_id):
		'''
		# get some id information just from id
		<h3>四叶草漏洞插件社区</h3>
		name="em_weixinhao">gh_ffddcb517e94</label
		class="sp-txt">发布漏洞插件社区最新动态</span>
		class="sp-txt"><a class="blue" target="_blank" id="sogou_vr_11002301_link_first_0" href="http://mp.weixin.qq.com/s?src=3&amp;timestamp=1474346138&amp;ver=1&amp;signature=cihj36rD5dWAYFgMIG-0OLRD5R1hg8WBrdXiuc*oUhgy8JCjWWBcxFvyjmU5H5lju7bWgPUjqbMrDtZY4-jb2J5fiwbC1qhn5AfLG*CyJCdrHLZg7fR2w3wQu5iQl5j*7Atoi4AVWwrTz30PsA*YAMpbH9sm6VukOgflmLv6i3g=">Microsoft Windows内核提权漏洞原理分析与利用(CVE-2016-3308 / ZDI</a><span
		'''

		feed_url = WXID_QUERY_URL.format(wx_id=wx_id)
		r=self.browser_url(feed_url)
		if not r:
			return False

		id_obj = {}
		id_obj["wx_id"] = re.findall(r"name=\"em_weixinhao\">(\S+)</label", r)[0].strip()
		if id_obj["wx_id"] != wx_id:
			return False
		# todo:all fuzz search..  maybe.. NO...
		# method parm:,exact=True
		# if not exact:

		id_obj["name"] = re.findall(r"h3>(\S+)<\/h3", r)[0].strip()
		id_obj["desc"] = re.findall(r"class=\"sp-txt\">(.*)</span>", r)[0].strip()
		id_obj["last_msg"] = re.findall(r"href=\"\S+\">(.*)</a><span\s+class=\"hui\">", r)[0].strip()

		for k in id_obj.iterkeys():
			id_obj[k]=unescape(id_obj[k])
			id_obj[k] = id_obj[k].replace("&nbsp_place_holder;", " ")


		return id_obj


	def get_info_by_url(self, wx_url):
		# shortcut
		# client = tornado.httpclient.HTTPClient()
		r = self.fetch_url_g(wx_url)
		wx_obj = self.get_info_by_html(r)
		return wx_obj

	def get_full_info_by_url(self, wx_url):
		r = self.fetch_url_g(wx_url)
		wx_full=self.get_full_info_by_html(r)
		return wx_full

	def get_full_info_by_html(self, html):
		wx_full=self.get_info_by_html(html).copy()
		wx_full.update(self.process_content(html,wx_full['msg_cover']))

		return wx_full


	def get_info_by_html(self, html):
		'''
		Main method to oprate
		Get all info from msg by given html

		'''
		r = html
		'''
				var nickname = "四叶草漏洞插件社区";
				var appmsg_type = "9";
				var ct = "1473139742";
				var publish_time = "2016-09-06" || "";
				var user_name = "gh_ffddcb517e94";
				var user_name_new = "";
				var fakeid   = "NjM1NjMwMjIz";
				var version   = "";
				var is_limit_user   = "0";
				var round_head_img = "http://mmbiz.qpic.cn/mmbiz/fHdFWFicUeItoIRvIGutxYfShnpWuhRke30GlT7WicnUhsvgoADstQbWe6tT6J9LnMke2L2hSwPG1Q2Ko5ib6PBFw/0?wx_fmt=png";
				var msg_title = "SSC安全峰会技术挑战赛，有技术，你就来";
				var msg_desc = "如何向大家证明你技术很NB？做给我们看！";
				var msg_cdn_url = "http://mmbiz.qpic.cn/mmbiz_jpg/fHdFWFicUeIuWbhgh5yIzrzdy0RJAvXvAdDbkVgPPXUF7bc4jkubQ3DJZ1WFIoocFFYb880cL5mOVQMME7MDiaDA/0?wx_fmt=jpeg";
				var msg_link = "http://mp.weixin.qq.com/s?__biz=MzI0MTE0MjYxOQ==&amp;mid=2649296192&amp;idx=1&amp;sn=ff4feb1afee87e400547efdc93518e41#rd";

				## detail msg info
				em class="rich_media_meta rich_media_meta_text">衡</em>
				<a class="rich_media_meta rich_media_meta_link rich_media_meta_nickname" href="javascript:void(0);" id="post-user">四叶草漏洞插件社区</a>
				<span class="rich_media_meta rich_media_meta_text rich_media_meta_nickname">四叶草漏洞插件社区</span>
				<div id="js_profile_qrcode" class="profile_container" style="display:none;">
				<div class="profile_inner">
				<strong class="profile_nickname">四叶草漏洞插件社区</strong>
				<img class="profile_avatar" id="js_profile_qrcode_img" src="" alt="">
				<p class="profile_meta">
				<label class="profile_meta_label">微信号</label>
				<span class="profile_meta_value"></span>
				<p class="profile_meta">
				<label class="profile_meta_label">功能介绍</label>
				<span class="profile_meta_value">发布漏洞插件社区最新动态</span>

				'''
		wx_obj = {}
		wx_id = re.findall(r"profile_meta_value\"\s?>(\S+)<\s?\/", r)
		# wx id & desc
		if len(wx_id) == 2:
			wx_obj['wx_id'] = wx_id[0].strip()
			wx_obj['desc'] = wx_id[1].strip()
		else:
			wx_obj['wx_id'] = re.findall(r"user_name\s?=\s?\"(\S+)\"\;", r)[0].strip()
			wx_obj['desc'] = re.findall(r"profile_meta_value\"\s?>(\S+)<\s?\/", r)[0].strip()
		# nickname
		wx_name = re.findall(r'var\snickname\s+=\s+\"(\S+)\"\;', r)
		wx_obj['name'] = wx_name[0].strip()

		# msg info
		wx_obj['msg_date'] = re.findall(r'var\spublish_time\s+=\s+\"(\S+)\"\s+\|\|', r)[0].strip()
		msg_ct=re.findall(r'var\sct\s+=\s+\"(\d+)\"\;', r)[0].strip()
		wx_obj['msg_createdtime'] =weixindate_fromTS(msg_ct)
		wx_obj['msg_title'] = re.findall(r'var\smsg_title\s+=\s+\"(\S+)\"\;', r)[0].strip()
		wx_obj['msg_desc'] = re.findall(r'var\smsg_desc\s+=\s+\"(\S+)\"\;', r)[0].strip()
		wx_obj['msg_cover'] = re.findall(r'var\smsg_cdn_url\s+=\s+\"(\S+)\"\;', r)[0].strip()
		wx_obj['msg_link'] = re.findall(r'var\smsg_link\s+=\s+\"(\S+)\"\;', r)[0].strip()
		wx_obj['msg_source'] = re.findall(r"msg_source_url\s+=\s+'(.*)'", r)[0].strip()
		author=re.findall(r'em\s+class=\"rich_media_meta\s+rich_media_meta_text\">(\S+)<', r)
		if author:
			wx_obj['msg_author'] = author[0].strip()
		else:
			wx_obj['msg_author'] = ""

		for k in wx_obj.iterkeys():
			wx_obj[k] = unescape(wx_obj[k])
			wx_obj[k] = wx_obj[k].replace("&nbsp_place_holder;"," ")

		return wx_obj

	def process_content(self, html,coverurl):

		root = Xhtml.fromstring(html)

		# 抽取文章内容
		try:
			content = root.xpath('//*[@id="js_content"]')[0]
		except IndexError:
			return ''

		# 处理图片链接
		# leaf 3个视图:1rss内容;2自己从网页中提取的内容;3原始网页
		for img in content.xpath('.//img'):
			if (not 'src' in img.attrib) and img.attrib.get('data-src'):
				img.attrib['src'] = img.attrib.get('data-src')

		'''
		# 抽取封面cover图片1,这个比gsdata封面清晰
		# # 不再需要,被msg_cdn_url字段取代
		# script = root.xpath('//*[@id="media"]/script/text()')
		# _COVER_RE = re.compile(r'cover = "(http://.+)";')
		# if script and _COVER_RE.findall(script[0]):
		# 	item_dict['msg_cover'] = _COVER_RE.findall(script[0])[0]
		'''

		# 插入封面到html
		if coverurl:
			coverelement = lxml.etree.Element('img')
			coverelement.set('src', coverurl)
			content.insert(0, coverelement)

		# 生成HTML
		content = lxml.html.tostring(content, encoding='unicode')
		# 清除垃圾,内容各式各样,不做次多余处理
		# content = content[:content.rfind("<hr")]+"</div>"
		wx_obj_c={}
		wx_obj_c['msg_content'] = content

		return wx_obj_c