# coding:utf-8

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import JAQ_URL

from base import jaqBaseHandler
from utils.jaq import process_list, process_content


class jaqHandler(jaqBaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.configure(None,max_clients=100)
        # 生成api url
        if 'tech' in self.request.uri:
            url = JAQ_URL.format(catid=4)
            title="阿里聚安全-技术研究"
        elif 'news' in self.request.uri:
            url = JAQ_URL.format(catid=17)
            title = "阿里聚安全-安全资讯"
        else:
            url=''
            self.redirect("/")
        # 访问api url,获取公众号文章列表
        request = tornado.httpclient.HTTPRequest(url=url)
        response = yield client.fetch(request)

        if not response.code == 200:
            self.redirect("/")

        rc = response.body.decode('utf-8')
        items = process_list(rc) # 解析文章列表

        if not items:
            self.set_header("Content-Type", "application/xml")
            self.render("rss.xml", title='', description='', items=items, pubdate='', link=url)

        # 爬取每篇文章的内容
        responses = yield [client.fetch(i['link'],raise_error=False) for i in items]
        for i, response in enumerate(responses):
            if response.code == 200:
                html = response.body.decode('utf-8')
                # build content
                items[i]= process_content(html,item_dict=items[i])
            else:
                items[i]['content'] = ''


        pubdate = items[0]['created']
        description = items[0]['author']

        self.set_header("Content-Type", "application/xml")
        self.render("rss.xml", title=title, description=description, items=items, pubdate=pubdate, link=url)
