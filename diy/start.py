import os, sys

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in sys.path:
    sys.path.insert(0, _basedir)

reload( sys )
sys.setdefaultencoding('utf-8')

import tornado.web

from jinja2_tornado import JinjaLoader
from urls import urls
from task import mc


# IP = os.environ['OPENSHIFT_DIY_IP']
# PORT = int(os.environ['OPENSHIFT_DIY_PORT'])
IP = '127.0.0.1'
PORT = '2103'


class Application(tornado.web.Application):
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
    tornado.ioloop.IOLoop.instance().start()
