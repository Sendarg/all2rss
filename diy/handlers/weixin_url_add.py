# coding:utf-8

import json,re
from urllib import quote_plus

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_GS_ADD_URL,GS_ADD_HEADERS,CACHE_URL_WX


class WeixinAddHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.HTTPClient()
        wx_url=self.request.uri[20:]
        gs_add_url=WEIXIN_GS_ADD_URL.format(url=quote_plus(wx_url))

        request = tornado.httpclient.HTTPRequest(url=gs_add_url, headers=GS_ADD_HEADERS)
        r=client.fetch(request).body.decode('utf-8').strip()
        rj=json.loads(r)
        if rj['error']==1:
            wx_info = self.get_msg(wx_url)
            alert="++++\tAdded:\t%s\n"%(wx_info['id']+":"+wx_info['name'])
            self.write(alert)
            self.write(json.dumps(wx_info,ensure_ascii=False))
            feed_url=CACHE_URL_WX.format(wx_id=wx_info['id'])
            self.write("\n++++\tRSS Feed URL:\t%s\n"%(feed_url))
        else:
            self.write("error")

    def get_msg(self,wx_url):
        client = tornado.httpclient.HTTPClient()
        r = client.fetch(wx_url).body.decode('utf-8').strip()

        wx_obj={}
        wx_id = re.findall(r"profile_meta_value\"\s?>(\S+)<\s?\/",r)
        wx_obj['id']=wx_id[0].strip()
        wx_name = re.findall(r'var\snickname\s+=\s+\"(\S+)\"\;',r)
        wx_obj['name'] = wx_name[0].strip()
        wx_title = re.findall(r'var\smsg_title\s+=\s+\"(\S+)\"\;', r)
        wx_obj['title'] = wx_title[0].strip()
        wx_desc = re.findall(r'var\smsg_desc\s+=\s+\"(\S+)\"\;', r)
        wx_obj['desc'] = wx_desc[0].strip()
        wx_pic = re.findall(r'var\smsg_cdn_url\s+=\s+\"(\S+)\"\;', r)
        wx_obj['pic'] = wx_pic[0].strip()
        wx_link = re.findall(r'var\smsg_link\s+=\s+\"(\S+)\"\;', r)
        wx_obj['link'] = wx_link[0].strip()
        return wx_obj