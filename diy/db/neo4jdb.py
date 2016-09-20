# coding:utf-8

from py2neo import Graph,Node,Relationship
from wx_data_lib import wx_info


class store2Neo(object):
	def __init__(self):
		self.neo4j = Graph(user='neo4j',password='neo4j')
		# wx_info is return from db.wx_info or combine together
	def create_WX_auto(self,wx_info):
		self.create_WX_ID(wx_info["wx_id"])
		self.create_WX_MSG_FULL(wx_info)

	def create_WX_ID(self,wx_id_info):
		'''
		CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
		CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
		'''
		WX_ID = self.neo4j.find_one("WX_ID", property_key="wx_id", property_value=wx_id_info['wx_id'])
		if WX_ID:
			print "---- WX_ID exists:\t%s"%WX_ID["wx_id"]
			return False
		else:
			wxid1 = Node("WX_ID")
			wxid1.update(wx_id_info)
			self.neo4j.create(wxid1)
			print "++++ WX_ID stored:\t%s" % wx_id_info['wx_id']
			return True


	def create_WX_MSG_FULL(self,wx_info):
		'''
		CREATE (Hugo)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix)

		wx_info['wx_id']
		wx_info['desc']
		wx_info['name']
		wx_info['last_msg']
		wx_info['msg_book']
		wx_info['msg_up']
		wx_info['msg_date']
		wx_info['msg_createdtime']
		wx_info['msg_title']
		wx_info['msg_desc']
		wx_info['msg_cover']
		wx_info['msg_link']
		wx_info['msg_source']
		wx_info['msg_author']
		wx_info['msg_content']

		# wx_id=wx_info['wx_id'],
		# desc=wx_info['desc'],
		# name=wx_info['name'],
		# last_msg=wx_info['last_msg'],
		# msg_book=wx_info['msg_book'],
		# msg_up=wx_info['msg_up'],
		# msg_date=wx_info['msg_date'],
		# msg_createdtime=wx_info['msg_createdtime'],
		# msg_title=wx_info['msg_title'],
		# msg_desc=wx_info['msg_desc'],
		# msg_cover=wx_info['msg_cover'],
		# msg_link=wx_info['msg_link'],
		# msg_source=wx_info['msg_source'],
		# msg_author=wx_info['msg_author'],
		# msg_content=wx_info['msg_content']


		'''

		WX_MSG = self.neo4j.find_one("WX_MSG", property_key="msg_link", property_value=wx_info['msg_link'])
		if WX_MSG:
			print "---- WX_MSG exists:\t%s" % WX_MSG["msg_link"]
			return False
		else:
			# msg=PropertyDict(wx_info)
			news1 = Node("WX_MSG")
			news1.update(wx_info)

			# create new node & relationship
			WX_ID = self.neo4j.find_one("WX_ID", property_key="wx_id", property_value=wx_info["wx_id"])
			if WX_ID:
				id_pub_news=Relationship(WX_ID,"pub",news1,pub_time=wx_info['msg_createdtime'])
				self.neo4j.create(id_pub_news)
				print "++++ WX_MSG stored:\t%s" % wx_info["msg_title"]
				return True
			else:
				print "---- WX_ID NOT exists:\t%s"  %wx_info["wx_id"]
				return False






def tesing():
	d={}
	d['wx_id'] = "read04"
	d['desc'] = "ddddddddddd"
	d['name'] = "dushu"
	d['last_msg'] = "dushu50ben"

	o={}
	o['msg_link']="http://mp.weixin.qq.com/s?__biz=MzIwNDA0NTczNA==&mid=2735122602&idx=3&sn=50a04a6b74e2449e6c71a87de2cca8de&chksm=b03424638743ad7531410bab7ccccac2c58a2c641d55b5d65b63432ecc2363ee5769682898c66b6&scene=4#wechat_redirect"
	o['msg_book']="msg_book"
	o['msg_up']="msg_up"
	o['wx_id']="read04"
	o['desc']="ddddddddddd"
	o['name']="dushu"
	o['last_msg']="dushu50ben"
	o['msg_date']="2016-11-12"
	o['msg_createdtime']="2016-11-12 12:21:12"
	o['msg_title']="mdddddddddddddddddd"
	o['msg_desc']="msg_desc"
	o['msg_cover']="msg_cover"
	o['msg_source']="msg_source"
	o['msg_author']="msg_author"
	o['msg_content']="msg_content"

	itemDict={'img':"http://111.txt",
	          'title':"kjnshuba",
	          'desc':"ddddddddddddddddddddddd",
	          'link':"http://2222",
	          'author':"yan.bo",
	          'created':"2016-11-12",
	          'book':12,
	          'up':10,
	          'cover':"http:/ddddddd",
	          'content':"ccccccccccccccccccccccccccccccccccccc"
	          }

	n=store2Neo()
	n.create_WX_ID(d)
	n.create_WX_MSG_FULL(o)

# tesing()