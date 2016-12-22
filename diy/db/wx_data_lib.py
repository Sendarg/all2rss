# coding:utf-8

from configs import WXID_QUERY_URL

from lxml import html as Xhtml
import lxml,re
from utils.date_format import weixindate_fromTS
from utils.iHttpLib import deEntities1

from requests import get
from utils.iHttpLib import browser_url



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

	def get_id_info_by_ID(self, wx_id):

		feed_url = WXID_QUERY_URL.format(wx_id=wx_id)
		r=browser_url(feed_url,expectTitle=u'的相关微信公众号 – 搜狗微信搜索')
		# http://weixin.sogou.com//new/pc/images/bg_404_2.png
		if (not r )or ("bg_404_2.png" not in  r):
			print "==== \tNo Search Results in URL:\t%s" % (feed_url)
			return False

		id_obj = {}
		try:
			id_obj["wx_id"] = re.findall("name=\"em_weixinhao\">(\S+)</label", r)[0].strip()
		except IndexError:
			print "ERRORERROR:IndexError:%s"%feed_url
		
		if not id_obj["wx_id"]:
			return False
		# todo : one method to remove specialy html label <em> for search keywords
		if id_obj["wx_id"][:4]=="<em>":
			id_obj["wx_id"]=id_obj["wx_id"][4:-5]
		if id_obj["wx_id"] != wx_id:
			return False
		# todo:all fuzz search..  maybe.. NO...
		# method parm:,exact=True
		# if not exact:

		# sougou 换了内容,重新匹配
		id_obj["name"] = re.findall("toweixin_account_name_0.*>(\S+)</a><i></i>", r)[0].strip()
		id_obj["desc"] = re.findall("<dd>(.*)</dd>", r)[0].strip()
		last=re.findall("toweixin_account_article_0.*href=\"(.*)\">(.*)</a>", r)
		# 从sougou获取到的link会过期,需要重新解析新的info
		# link = deEntities1(last[0][0].strip())
		# msg_info=self.get_info_by_url(link)
		id_obj["last_link"] =  last[0][0].strip()
		id_obj["last_msg"] = last[0][1].strip()
		id_obj["group"] = ""

		# not all need this only the link
		for k in id_obj.iterkeys(): # only the link
			id_obj[k]=deEntities1(id_obj[k])
		
		return id_obj
	
	def get_id_info_by_url(self, wx_url):
		wx_info=self.get_info_by_url(wx_url)
		if wx_info:
			id_obj={}
			id_obj["wx_id"]=wx_info["wx_id"]
			id_obj["name"]=wx_info["name"]
			id_obj["desc"]=wx_info["desc"]
			id_obj["last_link"]=wx_info["msg_link"]
			id_obj["last_msg"]=wx_info["msg_title"]
			id_obj["group"]=""
			
			return id_obj
		else:
			return False
		

	def get_info_by_url(self, wx_url):
		# shortcut
		# client = tornado.httpclient.HTTPClient()
		r = get(wx_url).content
		wx_obj = self.get_info_by_html(r)
		return wx_obj


	def get_full_info_by_url(self, wx_url):
		r = get(wx_url).content
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
		if not html:
			return False
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

		# wx id & desc,some id not set weixin ID so use user_name
		wx_id = re.findall("profile_meta_value\"\s?>(.*)<\s?\/", r) # 功能介绍 一样的标签,可能用空格
		if len(wx_id) == 2:
			wx_obj['wx_id'] = wx_id[0].strip()
			if  not wx_obj['wx_id']:
				wx_obj['wx_id'] = re.findall("user_name\s?=\s?\"(\S+)\"\;", r)[0].strip()
			wx_obj['desc'] = wx_id[1].strip()
		elif len(wx_id) == 1:
			wx_obj['wx_id'] = re.findall("user_name\s?=\s?\"(\S+)\"\;", r)[0].strip()
			wx_obj['desc'] = re.findall("profile_meta_value\"\s?>(\S+)<\s?\/", r)[-1].strip()
		else:
			return False
		# nickname
		wx_name = re.findall('var\snickname\s+=\s+\"(\S+)\"\;', r)
		wx_obj['name'] = wx_name[0].strip()

		# msg info
		wx_obj['msg_date'] = re.findall('var\spublish_time\s+=\s+\"(\S+)\"\s+\|\|', r)[0].strip()
		msg_ct=re.findall('var\sct\s+=\s+\"(\d+)\"\;', r)[0].strip()
		wx_obj['msg_createdtime'] =weixindate_fromTS(msg_ct)
		wx_obj['msg_title'] = re.findall('var\smsg_title\s+=\s+\"(.*)\"\;', r)[0].strip() # may have space
		wx_obj['msg_cover'] = re.findall('var\smsg_cdn_url\s+=\s+\"(\S+)\"\;', r)[0].strip()
		wx_obj['msg_link'] = re.findall('var\smsg_link\s+=\s+\"(.*)\"\;', r)[0].strip()
		wx_obj['msg_source'] = re.findall("msg_source_url\s+=\s+'(.*)'", r)[0].strip()
		if not wx_obj['msg_link']:
			wx_obj['msg_link']=wx_obj['msg_source']

		wx_obj['msg_desc'] = ""
		desc=re.findall('var\smsg_desc\s+=\s+\"(.*)\"\;',r)
		if desc:wx_obj['msg_desc'] = desc[0].strip()

		wx_obj['msg_author'] = ""
		author=re.findall('em\s+class=\"rich_media_meta\s+rich_media_meta_text\">(\S+)<', r)
		if author:wx_obj['msg_author'] = author[0].strip()

		# sougou的输出确实有实体编码。另外需要在输出控制
		for k in wx_obj.iterkeys():
			wx_obj[k] = deEntities1(wx_obj[k])

		return wx_obj


	def process_content(self, html,coverurl):

		root = Xhtml.fromstring(html)

		# 抽取文章内容
		content = root.xpath('//*[@id="js_content"]')[0]
		# try:
		#
		# except IndexError:
		# 	return ''

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



url="http://mp.weixin.qq.com/s?timestamp=1474516462&src=3&ver=1&signature=I6NlWsM0KyZWEM12N89mqOzVHOXBdJlRT3nBc8OGPc6Av3BnxarDYVVB0c9625i9HeTEnRlXoOtFbiJg9UJjYBWmV1iVwwwfVftM1kZo4*C*TJjHEnzlUakEVTzor38YHtkh5x297NTVAcq9hDuWPKZg5*9gyphH0klQShaylVg="

# wx_info().fetch_url_g(url)
