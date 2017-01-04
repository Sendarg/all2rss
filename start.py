# coding:utf-8

import os, sys, re

reload(sys)
sys.setdefaultencoding('utf-8')

basedir = os.path.abspath(os.path.dirname(__file__))
macNoSIP = '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python'
if basedir not in sys.path:
	sys.path.insert(0, basedir)
if macNoSIP not in sys.path:
	sys.path.insert(0, macNoSIP)

from tornado import web, ioloop
from jinja2_tornado import JinjaLoader
from urls import urls
from task import sync_rss_feeds
from configs import Server_IP, PORT, CACHE_PERIODIC
from db.wx_id import manage_WX_ID


# import memcache
# mc = memcache.Client(['%s:15211' % IP])


class Application(web.Application):
	def __init__(self, **kwargs):
		# self.mc = mc
		# self.neo4j=Neo4j()
		super(Application, self).__init__(**kwargs)


application = Application(
	# debug=True,
	handlers=urls,
	static_path=os.path.join(basedir, 'static'),
	template_loader=JinjaLoader(os.path.join(basedir, 'templates'),
	                            autoescape=True, extensions=['jinja2.ext.autoescape']),
	# autoescape=False,容易引起格式问题,而客户端无法解析
)

if __name__ == "__main__":
	application.listen(PORT,Server_IP)
	## first start init some basic  data (cyber)
	if len(manage_WX_ID().list_WX_ID()) == 0:
		File_rss = "opml/Subscriptions.opml"
		if manage_WX_ID().mass_Import_WX_ID_from_opml(File_rss):
			print "==== Defaults WX_ID Imported!"
	
	print "== auto sync rss news"
	# ioloop.IOLoop().call_later(5.0, sync_rss_feeds)
	# ioloop.IOLoop().run_sync(sync_rss_feeds)
	# ioloop.PeriodicCallback(sync_rss_feeds, (30 * 60+10) * 1000).start() # sync every 30minutes+10s
	ioloop.PeriodicCallback(sync_rss_feeds, CACHE_PERIODIC).start()
	ioloop.IOLoop.instance().start()
