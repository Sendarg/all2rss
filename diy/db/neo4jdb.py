from py2neo import Graph,Node,Relationship

class Neo4j(object):
	def __init__(self):
		self.neo4j = Graph(user='neo4j',password='neo4j')

	def create_source(self,wxid,desc):
		'''
		CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
		CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
		'''
		WXID = self.neo4j.find_one("WXID", property_key="wxid", property_value=wxid)
		if WXID:
			print "---- Node exists: %s"%WXID["wxid"]
			return False
		else:
			WXID1 = Node("WXID",
			             wxid=wxid,
			             desc=desc
			             )
			self.neo4j.create(WXID1)



	def create_news(self,wxid,itemDict):
		'''
		CREATE (Hugo)-[:ACTED_IN {roles:['Neo']}]->(TheMatrix)
		o['img'] =
		o['title']
		o['desc'] =
		o['link'] =
		o['author']
		o['created'
		o['book'] =
		o['up'] = r
		cover
		content
		'''
		o=itemDict
		WXNEWS = self.neo4j.find_one("WXNews", property_key="link", property_value=o['link'])
		if WXNEWS:
			print "---- News exists: %s" % WXNEWS["link"]
			return False
		else:
			news1 = Node("WXNews",
			             title=o['title'],
			             desc=o['desc'],
			             link=o['link'],
			             author=o['author'],
			             created=o['created'],
			             book=o['book'],
			             up=o['up'],
			             cover=o['cover'],
			             content=o['content']
			             )
			# create new node & relationship
			WXID=self.neo4j.find_one("WXID",property_key="wxid",property_value=wxid)
			if WXID:
				id_pub_news=Relationship(WXID,"pub",news1,pub_date=o['created'])
				self.neo4j.create(id_pub_news)
			else:
				print "---- WXID NOT exists: %s"  %WXID["wxid"]
				return False






def tesing():
	n=Neo4j()
	n.create_source('read02',u'dusuh')
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
	n.create_news('read02',itemDict)