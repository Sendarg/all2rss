# coding: utf-8

import tornado.gen
import tornado.httpclient
from configs import RSS_LIST_FILE,OPENSHIFT_WX_URL,OPENSHIFT_URL


@tornado.gen.coroutine
def sync_rss_feeds():
    client = tornado.httpclient.AsyncHTTPClient()
    for key in open(RSS_LIST_FILE).readlines():
        key=key.strip()
        if key:
            if key.startswith("wx__"):
                url = OPENSHIFT_WX_URL.format(wxid=key[4:])
            else:
                url=OPENSHIFT_URL.format(key=key)
            request = tornado.httpclient.HTTPRequest(url=url)
            requests=yield client.fetch(request)
            if requests:
                print "==== Synced feeds:\t%s"%url