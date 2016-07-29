# coding:utf-8

import json
from urllib import quote_plus

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_ADD_URL,ADD_HEADERS



class WeixinAddHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.HTTPClient()
        wx_url=self.request.uri[20:]
        gs_add_url=WEIXIN_ADD_URL.format(url=quote_plus(wx_url))

        request = tornado.httpclient.HTTPRequest(url=gs_add_url,headers=ADD_HEADERS)
        r=client.fetch(request).body.decode('utf-8').strip()
        rj=json.loads(r)
        if rj['error']==1:
            # self.render_string()
            print "++++	Added URL\t[%s] ----"%wx_url