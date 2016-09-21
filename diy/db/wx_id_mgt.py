# coding:utf-8

from db.wx_data_lib import wx_info
from db.neo4jdb import store2Neo


def check_ID(wx_id):
	if not store2Neo().is_WX_ID_Exists(wx_id):
		id_info = wx_info().get_id_info(wx_id)
		if not id_info:
			print "----\t[ %s ]\t帐号已注销或被封" % wx_id
			return False
		else:
			store2Neo().create_WX_ID(id_info)
	return True