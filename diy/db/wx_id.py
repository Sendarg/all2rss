# coding:utf-8

from db.wx_data_lib import wx_info
from py2neo import Graph,Node,ConstraintError
from utils.iHttpLib import deEntiesListDict





class manage_WX_ID(object):
	def __init__(self):
		self.neo4j = Graph(user='neo4j', password='111')
	
	def list_WX_ID(self):
		list = self.neo4j.data('MATCH (w:WX_ID) RETURN w order by w.last_date desc')
		list=deEntiesListDict(list)
		return list
	
	def list_WX_KEYS(self):
		list = self.neo4j.data('MATCH (w:WX_ID) RETURN w.wx_id as wid order by w.last_date desc')
		for l in list:
			yield "wx__"+l["wid"]
	
	def count_WX_MSG(self,wx_id):
		count = self.neo4j.data('MATCH (w:WX_MSG) where w.wx_id="%s" RETURN count(w) as c'%wx_id)
		return count[0]["c"]
	
	def is_WX_ID_Exists(self, wx_id):
		WX_ID = self.neo4j.find_one("WX_ID", property_key="wx_id", property_value=wx_id)
		if WX_ID:
			# print "---- WX_ID exists:\t%s" % WX_ID["wx_id"] # too much useless info
			return True
		else:
			return False
	
	def check_ID(self, wx_id):
		if not self.is_WX_ID_Exists(wx_id):
			id_info = wx_info().get_id_info_by_ID(wx_id)
			if not id_info:
				print "----\t[ %s ]\t帐号不存在(无查询结果|已注销|被封)" % wx_id
				return False
			else:
				self.create_WX_ID(id_info)
		return True
	
	def create_WX_ID(self, wx_id_info):
		'''
		CREATE (TheMatrix:Movie {title:'The Matrix', released:1999, tagline:'Welcome to the Real World'})
		CREATE (Hugo:Person {name:'Hugo Weaving', born:1960})
		'''
		if not self.is_WX_ID_Exists(wx_id_info['wx_id']):
			wxid1 = Node("WX_ID")
			wxid1.update(wx_id_info)
			self.neo4j.create(wxid1)
			print "++++ WX_ID stored:\t%s" % wx_id_info['wx_id']
			return True
		
	def del_WX_ID(self, wx_id):
		WX_ID = self.neo4j.find_one("WX_ID", property_key="wx_id", property_value=wx_id)
		try:
			self.neo4j.delete(WX_ID)
			print "==== WX_ID Deleted!"
		except ConstraintError:
			del_cyber = "MATCH (w:WX_ID)-[r]->(m:WX_MSG) where w.wx_id='%s' delete w,r,m" % wx_id
			self.neo4j.run(del_cyber)
			print "==== All Nodes and Relationships Deleted!!"
		return True
						
	def update_WX_ID(self):
		
		# neo4j.run return Cursor buffer Record one by one
		# neo4j.data return  Data Dict list
		wx_ids = self.neo4j.run("MATCH (w:WX_ID) RETURN w.wx_id")
		# wx_ids2 = self.neo4j.data("MATCH (w:WX_ID) RETURN w.wx_id")
		for wid in wx_ids:
			# update WX_ID info
			WX_ID = self.neo4j.find_one("WX_ID", property_key="wx_id", property_value=wid)
			
			# get last id count info
			count_cyber = 'MATCH (w:WX_MSG) where w.wx_id="%s" RETURN count(w) as msg_count' % wid
			count = self.neo4j.data(count_cyber)[0]
			
			if count["msg_count"] == 0:
				print "---- WX_ID Has Nothing:\t%s" % wid
				WX_ID.update(count)
				self.neo4j.push(WX_ID)
				break
			
			# get last message info
			last_cyber = 'MATCH (w:WX_MSG) where w.wx_id="%s" RETURN w.msg_date as last_date,w.msg_title as last_msg,w.msg_link as last_link order by w.msg_date desc  limit 1' % wid
			last = self.neo4j.data(last_cyber)[0]
			
			WX_ID.update(last)
			WX_ID.update(count)
			self.neo4j.push(WX_ID)
			
			print "==== WX_ID updated:\t%s" % wid


	
	

# n =
#
# print manage_WX_ID().list_WX_ID()