# coding:utf-8

from configs import FEED_HIS_FILE



def get_list():
    lists=[]
    FILE=open(FEED_HIS_FILE,"r")
    for key in FILE.readlines():
        key=key.strip()
        if key and key[:1]!="#":
            lists.append(key)
    FILE.close()
    return lists


def update_feeds(key):
    lists=get_list()
    FILE = open(FEED_HIS_FILE, "a")
    if key not in lists:
        FILE.writelines("\n"+key)
    FILE.close()
    return True