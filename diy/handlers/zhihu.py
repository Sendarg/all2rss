# coding:utf-8

import tornado.gen
import tornado.httpclient
import tornado.web
from configs import ZHIHU_URL, ZHIHU_HEAD

from base import ZhihuBaseHandler
from utils.zhihu import process_list,process_content


class ZhihuHandler(ZhihuBaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.configure(None, max_clients=100)
        response = yield client.fetch(ZHIHU_URL)
        if not response.code == 200:
            self.redirect("/")
        items=process_list(response.body.decode('utf-8'))

        responses = yield [client.fetch(i['json_url'], headers=ZHIHU_HEAD) for i in items]
        for i, response in enumerate(responses):
            if response.code == 200:
                body=response.body.decode('utf-8')
                items[i]=process_content(body,items[i])
            else:
                items[i]['author'] = 'zhihu'
                items[i]['content'] = ''

        title = u'知乎日报'
        description = u'在中国,以独有的方式为你提供最高质、最深度、最有收获的阅读体验。'
        pubdate = items[0]['created']
        link = 'http://daily.zhihu.com/'
        self.set_header("Content-Type", "application/xml")
        self.render("rss.xml", title=title, description=description, items=items, pubdate=pubdate, link=link)