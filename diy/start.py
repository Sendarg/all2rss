import os, sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

reload( sys )
sys.setdefaultencoding('utf-8')


from tornado import web,ioloop
from jinja2_tornado import JinjaLoader
from urls import urls


from task import sync_rss_feeds
import memcache
from configs import IP,PORT


mc = memcache.Client(['%s:15211' % IP])

class Application(web.Application):
    def __init__(self, **kwargs):
        self.mc = mc
        super(Application, self).__init__(**kwargs)


application = Application(
    handlers=urls,
    static_path=os.path.join(_basedir, 'static'),
    template_loader=JinjaLoader(os.path.join(_basedir, 'templates'),
        autoescape=True, extensions=['jinja2.ext.autoescape']),
)

if __name__ == "__main__":
    application.listen(PORT, IP)
    print "== auto sync rss news"
    # ioloop.IOLoop().call_later(5.0, sync_rss_feeds)
    # ioloop.IOLoop().run_sync(sync_rss_feeds)
    ioloop.PeriodicCallback(sync_rss_feeds, 6 * 1000).start()
    # ioloop.PeriodicCallback(sync_rss_feeds, (30 * 60+10) * 1000).start() # sync every 30minutes+10s
    ioloop.IOLoop.instance().start()