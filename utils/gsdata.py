# encoding:utf-8
from utils.iHttpLib import post_GS
import json




def listGroup():
	url="http://index.gsdata.cn/private/wxnum/nickname/list"
	data="groupid=45623&type=0&keyword=&page=1&rows=1000"
	
	response=post_GS(url,data)
	list=json.loads(response)
	
	return list


def gs_info_by_name(keyword):
	url = "http://index.gsdata.cn/private/wxnum/nickname/list"
	data = "groupid=45623&type=0&keyword={keyword}&page=1&rows=1000"
	
	response = post_GS(url, data.format(keyword=keyword))
	list = json.loads(response)
	
	return list["rows"][0]["id"]


def delWX_by_id(id):
	url="http://index.gsdata.cn/private/wxnum/nickname/deleteIds?ids={ids}&groupid=45623"
	response=post_GS(url.format(ids=id))
	if response.content=="true":
		return True
	else:
		return False


def delWX_by_name(name):
	ids=gs_info_by_name(keyword=name)
	if delWX_by_id(ids) == "true":
		return True
	else:
		return False

