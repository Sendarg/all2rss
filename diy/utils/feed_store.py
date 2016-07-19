# coding:utf-8

from diy.configs import FEED_HIS_FILE



def get_list():
    lists=[]
    FILE=open(FEED_HIS_FILE,"r")
    for key in FILE.readlines():
        if key and key[:1]!="#":
            lists.append(key.strip())
    FILE.close()
    return lists


def update_feeds(key):
    lists=get_list()
    FILE = open(FEED_HIS_FILE, "r+")
    if key not in lists:
        FILE.writelines(key + "\n")
        FILE.close()
        return True
    else:
        return False