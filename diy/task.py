# coding: utf-8

import tornado.gen
import tornado.httpclient

from configs import CACHE_URL_WX,CACHE_URL,TIMEOUT,_HEADERS
from db.feed_store_File import get_list


@tornado.gen.coroutine
def sync_rss_feeds():
    client = tornado.httpclient.AsyncHTTPClient()
    for key in get_list():
        if key.startswith("wx__"):
            url = CACHE_URL_WX.format(wx_id=key[4:])
        else:
            url=CACHE_URL.format(key=key)
        request = tornado.httpclient.HTTPRequest(url=url,headers=_HEADERS)
        requests= yield  client.fetch(request,
                                      connect_timeout=TIMEOUT,
                                      request_timeout=TIMEOUT
                                      )
        if requests:
            print "++++ Synced feeds:\t%s"%url
        else:
            print "---- Sync Failed:\t%s" % url