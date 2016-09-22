# coding:utf-8

from  tornado.httpclient import AsyncHTTPClient
from  tornado.httpclient import HTTPRequest,HTTPResponse
from  tornado.httputil import HTTPHeaders
from configs import _HEADERS, TIMEOUT



def getAClient(max_clients=400):
	client = AsyncHTTPClient(max_clients=max_clients)  # page 20 * size 20,
	client.configure(None,
	                 # "tornado.curl_httpclient.CurlAsyncHTTPClient",
	                 raise_error=False
	                 )
	return client

'''
# fuck TypeError: 'Future' object is not iterable
# may be can't be method lonely

import tornado.web
import tornado.gen
@tornado.gen.coroutine
def iAsynRequests(self,urlList):
	# 1000clients  &  100page no many error more by single page first request
	# now default set :  20page*20url
	# AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient") # seem many error

	reqs=[]
	for u in urlList:
		request = HTTPRequest(url=u,
		                      headers=_HEADERS,
		                      connect_timeout=TIMEOUT,
		                      request_timeout=TIMEOUT
		                      )
		reqs.append(request)

	client = AsyncHTTPClient(max_clients=self.max_clients)  # page 20 * size 20,
	client.configure(None,
	                      # "tornado.curl_httpclient.CurlAsyncHTTPClient",
	                      raise_error=False
	                      )

	yield [client.fetch(r for r in reqs)]
'''

def reqsBuilder(urlList):
	# 1000clients  &  100page no many error more by single page first request
	# now default set :  20page*20url
	# AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient") # seem many error
	Headers=HTTPHeaders(_HEADERS)

	reqs=[HTTPRequest(url=u,
	                  headers=Headers,
	                  connect_timeout=TIMEOUT,
	                  request_timeout=TIMEOUT
	                  )for u in urlList]
	return reqs