# coding:utf-8

import json

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_KEY, WEIXIN_URL,WEIXIN_COVER_URL,WEIXIN_HEADERS,TIMEOUT

from base import WeixinBaseHandler
from utils.weixin_gs import process_list, process_content


class WeixinHandler(WeixinBaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.configure(None,max_clients=500)
        wxid = self.key[4:]
        link = WEIXIN_KEY.format(id=wxid)
        url = WEIXIN_URL.format(id=wxid) # 生成api url

        # 访问api url,获取公众号文章列表
        request = tornado.httpclient.HTTPRequest(url=url)
        response = yield client.fetch(request,headers=WEIXIN_HEADERS,)

        if not response.code == 200:
            self.redirect("/")

        rc = response.body.decode('utf-8')
        items = process_list(rc) # 解析文章列表

        if items:
            # 获取每一个文章的封面
            coverResponses = yield [client.fetch(WEIXIN_COVER_URL.format(hash=i['img']),
                                                 # raise_error=False,
                                                 # connect_timeout=TIMEOUT,
                                                 # request_timeout=TIMEOUT,
                                                 headers=WEIXIN_HEADERS
                                                 ) for i in items]
            for i, response in enumerate(coverResponses):
                coverurl = None
                if response.code == 200 and response.body.decode('utf-8'):
                    rc = json.loads(response.body.decode('utf-8'))
                    if rc and dict(rc).has_key('url'):
                        coverurl = rc['url']
                items[i]['cover']=coverurl

            # 爬取每篇文章的内容
            responses = yield [client.fetch(i['link'],raise_error=False) for i in items]
            for i, response in enumerate(responses):
                if response.code == 200:
                    html = response.body.decode('utf-8')
                    # build content
                    items[i] = process_content(html,item_dict=items[i])
                else:
                    items[i]['content'] = ''

            pubdate = items[0]['created']
            title = description = items[0]['author']

            self.set_header("Content-Type", "application/xml")
            self.render("rss.xml", title=title, description=description, items=items, pubdate=pubdate, link=link)
        else:
            self.redirect("/")
            # self.set_header("Content-Type", "application/xml")
            # self.render("rss.xml", title='', description='', items=items, pubdate='', link=link)