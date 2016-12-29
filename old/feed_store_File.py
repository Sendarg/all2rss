# coding:utf-8
import os

# rss list story file
# No longer need,just for Neo4j,Only keep for remember
_dir = os.path.abspath(os.path.dirname(__file__))
FEED_HIS_FILE = os.path.join(_dir, 'feed_history.txt')



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