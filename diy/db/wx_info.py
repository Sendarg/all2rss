# coding:utf-8
import re
import tornado.httpclient
from configs import WXID_QUERY_URL



client = tornado.httpclient.HTTPClient()

def get_info_by_id(wx_id):
	'''
	<h3>四叶草漏洞插件社区</h3>
	name="em_weixinhao">gh_ffddcb517e94</label
	class="sp-txt">发布漏洞插件社区最新动态</span>
	class="sp-txt"><a class="blue" target="_blank" id="sogou_vr_11002301_link_first_0" href="http://mp.weixin.qq.com/s?src=3&amp;timestamp=1474346138&amp;ver=1&amp;signature=cihj36rD5dWAYFgMIG-0OLRD5R1hg8WBrdXiuc*oUhgy8JCjWWBcxFvyjmU5H5lju7bWgPUjqbMrDtZY4-jb2J5fiwbC1qhn5AfLG*CyJCdrHLZg7fR2w3wQu5iQl5j*7Atoi4AVWwrTz30PsA*YAMpbH9sm6VukOgflmLv6i3g=">Microsoft Windows内核提权漏洞原理分析与利用(CVE-2016-3308 / ZDI</a><span
	'''

	feed_url = WXID_QUERY_URL.format(wx_id=wx_id)
	r = client.fetch(feed_url).body.decode('utf-8').strip()

	id_obj = {}
	id_obj["name"] = re.findall(r"h3>(\S+)<\/h3", r)[0].strip()
	id_obj["wx_id"] = re.findall(r"name=\"em_weixinhao\">(\S+)</label", r)[0].strip()
	id_obj["desc"] = re.findall(r"class=\"sp-txt\">(\S+)</span>", r)[0].strip()
	id_obj["last_msg"] = re.findall(r"href=\"\S+\">(.*)</a><span\s+class=\"hui\">", r)[0].strip()

	return id_obj

def get_info_by_url(wx_url):

	# get full info from url
	# client = tornado.httpclient.HTTPClient()
	r = client.fetch(wx_url).body.decode('utf-8').strip()
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
		wx_obj['id'] = wx_id[0].strip()
		wx_obj['desc'] = wx_id[1].strip()
	else:
		wx_obj['id'] = re.findall(r"user_name\s?=\s?\"(\S+)\"\;", r)[0].strip()
		wx_obj['desc'] = re.findall(r"profile_meta_value\"\s?>(\S+)<\s?\/", r)[0].strip()
	# nickname
	wx_name = re.findall(r'var\snickname\s+=\s+\"(\S+)\"\;', r)
	wx_obj['name'] = wx_name[0].strip()

	# msg info
	wx_obj['msg_pubtime'] = re.findall(r'var\spublish_time\s+=\s+\"(\S+)\"\s+\|\|', r)[0].strip()
	wx_obj['msg_title'] = re.findall(r'var\smsg_title\s+=\s+\"(\S+)\"\;', r)[0].strip()
	wx_obj['msg_desc'] = re.findall(r'var\smsg_desc\s+=\s+\"(\S+)\"\;', r)[0].strip()
	wx_obj['msg_pic'] = re.findall(r'var\smsg_cdn_url\s+=\s+\"(\S+)\"\;', r)[0].strip()
	wx_obj['msg_link'] = re.findall(r'var\smsg_link\s+=\s+\"(\S+)\"\;', r)[0].strip()
	wx_obj['msg_source'] = re.findall(r"msg_source_url\s+=\s+'(.*)'", r)[0].strip()
	wx_obj['msg_author'] = re.findall(r'em\s+class=\"rich_media_meta\s+rich_media_meta_text\">(\S+)<', r)[0].strip()


	return wx_obj