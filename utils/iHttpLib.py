# coding:utf-8
from  tornado.httpclient import AsyncHTTPClient,HTTPClient
from  tornado.httpclient import HTTPRequest,HTTPResponse
from  tornado.httputil import HTTPHeaders

from geventhttpclient import HTTPClient as gHTTPClient
from geventhttpclient.url import URL

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configs import _HEADERS, TIMEOUT,GS_Session_HEADERS

from requests import get
from BeautifulSoup import BeautifulStoneSoup


		
def deEntities1(html):
	if type(html)==str or type(html)==unicode:
		#
		html= html.replace("\\x26amp;", "&")
		html = html.replace("\\x26quot;", "\"")
		html = html.replace("\\x26#39;", "\'")
		html = html.replace("\\x26nbsp;", " ")
		html = html.replace("\\x26gt;", ">")
		html = html.replace("\\x26lt;", "<")
		# delete real \ char fuck NO!
		# html = html.replace("\\", "")
		# some time left
		html = html.replace("amp;", "")
	
	return html


def deEntiesListDict(list):
	out = []
	for l in list:
		if l.has_key("w"):
			l = l['w']
		for k in l.iterkeys():
			l[k] = deEntities1(l[k])
		out.append(l)
	return out


def deEntities0(html):
	# fuck \\x26  "\\"这个时候是字符不是转义
	# 另外这个方法对整个html生效,但为了效率不使用
	if type(html) == str or type(html) == unicode:
		# html=str(html).replace("\\\\x","\\x")
		html = unicode(BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))
		# html = HTMLParser().unescape(html)
		# html = html.replace("&nbsp_place_holder;", " ")
	
	return html
	
	
	

def getAClient(max_clients=200):
	client = AsyncHTTPClient(max_clients=max_clients)  # page 20 * size 20,maybe great
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


def reqsBuilder(urlList,_HEADERS=_HEADERS):
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



def get_GS(url):
	client = HTTPClient()
	request = HTTPRequest(url, headers=GS_Session_HEADERS)
	r = client.fetch(request).body.decode('utf-8').strip()
	client.close()
	return r

def get1_GS(url):
	response = get(url=url, headers=GS_Session_HEADERS)
	r = response.content
	
	response.close()
	return r



def fetch_url_g_error(url):
	# todo:wait to fix bug
	# r=HTTPClient.get()

	url = URL(url)
	http = gHTTPClient(url.host,headers=_HEADERS)
	response = http.get(url.request_uri)
	if not response.status_code==200:
		print "----\tResponse Code[%s]\t%s" %(response.status_code, url)
		return False

	body = response.read() # eror in encoding
	r=body.decode('utf-8').strip()
	http.close()
	return  r



def browser_url(url,expectTitle):
	# todo : better code stratur(Proxy and Head) and beautiful;
	# try to anti antispider
	''' Can't Seting headers
	User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 Safari/538.1
	Cookie: ABTEST=0|1474465348|v1; IPLOC=CN3100; SUID=B7F39AB42441900A0000000057E28E44; PHPSESSID=1oflgi4l3d4ag6dba32cr6k1s4; SUIR=1474465348
	Connection: close
	Accept-Encoding: gzip, deflate
	Accept-Language: zh-CN,en,*
	Host: weixin.sogou.com


	User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2866.0 Safari/537.36
	Accept-Encoding: gzip, deflate, sdch
	Accept-Language: zh-CN,zh;q=0.8,he;q=0.6
	Connection: close
	'''
	'''
	PROXY='127.0.0.1:8080'
	webdriver.DesiredCapabilities.PHANTOMJS['proxy']={
		"httpProxy": PROXY,
		"ftpProxy": PROXY,
		"sslProxy": PROXY,
		"noProxy": None,
		"proxyType": "MANUAL",
		"class": "org.openqa.selenium.Proxy",
		"autodetect": False
	}
	'''

	driver = webdriver.PhantomJS()
	for i in range(2):# force retry will help
		driver.get(url)
		wait = WebDriverWait(driver, 10)
		# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'weixin-public')))
		wait.until(EC.presence_of_all_elements_located)
		driver.get(url) # twice will helpful
		print "====\t%s"%driver.title
		if expectTitle in driver.title:
			break
		else:
			print "----\tAntiSpider Error[%d] URL:\t%s" % (i+1,driver.current_url)

	r=driver.page_source
	driver.quit()

	return r
