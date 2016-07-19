# coding: utf-8

import tornado.gen
import tornado.httpclient
from configs import CACHE_URL_WX,CACHE_URL,TIMEOUT,_HEADERS
from utils.feed_store import get_list


@tornado.gen.coroutine
def sync_rss_feeds():
    client = tornado.httpclient.AsyncHTTPClient()
    for key in get_list():
        if key.startswith("wx__"):
            url = CACHE_URL_WX.format(wxid=key[4:])
        else:
            url=CACHE_URL.format(key=key)
        request = tornado.httpclient.HTTPRequest(url=url)
        requests= yield  client.fetch(request,
                                      connect_timeout=TIMEOUT,
                                      request_timeout=TIMEOUT,
                                      headers=_HEADERS)
        if requests:
            print "++++ Synced feeds:\t%s"%url
        else:
            print "---- Sync Failed:\t%s" % url