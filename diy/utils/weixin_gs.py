# coding:utf-8

from lxml import html as Xhtml
# from date_format import weixindate


def process_list(r):
	root = Xhtml.fromstring(r)
	list_len = len(root.xpath('//*[@class="article-ul"]/li'))
	out = []
	for i in range(list_len ):
		i=i+1
		o = {}
		# o['msg_img'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[1]/a/img')[0].attrib['data-hash']
		'''
		# 注释暂时用不上的属性,与后面可以从微信页面获取的内容重复操作
		o['msg_title'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/h4/a')[0].text
		o['msg_desc'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/a')[0].text
		o['msg_author'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/a/span')[0].text
		createDate = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/span[1]')[0].text[5:]
		o['msg_createdtime']=weixindate(createDate)
		'''
		o['msg_link'] = root.xpath('//*[@class="article-ul"]/li[' + str(i) + ']/div[2]/h4/a')[0].attrib['href']
		o['msg_book'] = root.xpath('//*[@class="article-ul"]/li[' + str(i) + ']/div[2]/div/font/text()[3]')[0].strip()
		o['msg_up'] = root.xpath('//*[@class="article-ul"]/li[' + str(i) + ']/div[2]/div/font/text()[2]')[0].strip()
		out.append(o)

	return out
