from db.wx_id import manage_WX_ID
import re

File_rss="opml/Subscriptions.opml"

defaultRss=open(File_rss,"r").read()
wx_ids=re.findall("weixin\?id=(\S+)\"", defaultRss)
manage_WX_ID().create_Batch_WX_ID_Simple(wx_ids)