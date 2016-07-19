# coding:utf-8

import json

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import WEIXIN_URL,WEIXIN_URL_PAGE,WEIXIN_COVER_URL,_HEADERS,TIMEOUT

from base import WeixinBaseHandler
from utils.weixin_gs import process_list, process_content


class WeixinHandler(WeixinBaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        clientAsync = tornado.httpclient.AsyncHTTPClient()
        clientAsync.configure(None, max_clients=2000)  # max error
        client = tornado.httpclient.HTTPClient()

        id = self.key[4:]
        link = WEIXIN_URL.format(id=id)

        # 访问api url,获取公众号文章列表,同步逐个获取
        items=[]
        for p in range(self.page_size):# 读取X页结果,第一次获取5页结果,第二次获取一页结果?
            url = WEIXIN_URL_PAGE.format(id=id,page=p)  # 生成api url
            print "++++	Processing WeiXin\t[%s]++++" % url
            request = tornado.httpclient.HTTPRequest(url=url,headers=_HEADERS)
            response =  client.fetch(request,
                                      # raise_error=False,
                                      connect_timeout=TIMEOUT,
                                      request_timeout=TIMEOUT
                                      )

            if response.code == 200:
                rc = response.body.decode('utf-8')
                [items.append(i) for i in process_list(rc)]# 解析文章列表
            else:
                print "----	Faile URL\t[%s] ----" % url

        if items :
            # 获取每一个文章的封面
            # for xinshengdaxue on openshift Code 500? ???
            # yield clientAsync
            coverResponses =  yield [clientAsync.fetch(WEIXIN_COVER_URL.format(hash=i['img']),
                                                 # raise_error=False,
                                                 connect_timeout=TIMEOUT,
                                                 request_timeout=TIMEOUT,
                                                 headers=_HEADERS
                                                 ) for i in items]
            for i, response in enumerate(coverResponses):
                coverurl = None
                if response.code == 200 and response.body.decode('utf-8'):
                    rc = json.loads(response.body.decode('utf-8'))
                    if rc and dict(rc).has_key('url'):
                        coverurl = rc['url']
                items[i]['cover']=coverurl

            # 爬取每篇文章的内容
            responses =   yield [clientAsync.fetch(i['link'],
                                                 # raise_error=False
                                                 ) for i in items]
            for i, response in enumerate(responses):
                if response.code == 200:
                    html = response.body.decode('utf-8')
                    # build content
                    items[i] = process_content(html,item_dict=items[i])
                else:
                    items[i]['content'] = ''

            # check item's <description><![CDATA[]]></description>
            if items[1]['content']:
                pubdate = items[0]['created']
                title = description = items[0]['author']

                self.set_header("Content-Type", "application/xml")
                self.render("rss.xml", title=title, description=description, items=items, pubdate=pubdate, link=link)
            else:
                self.redirect("/")
        else:
            self.redirect("/")