# coding:utf-8

import tornado.web

from configs import ZHIHU_EXPIRES, WEIXIN_EXPIRES,JAQ_EXPIRES,BASE_URL,WEIXIN_PAGE_SIZE
from utils.feed_store import update_feeds,get_list


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.key=""
        self.expires=""
        # self.mc = self.application.mc
        self.redisDB = self.application.redisDB
        self.url=BASE_URL+self.request.uri

    def prepare(self):
        '''
        预处理从缓存中获取html,如果能拿到,直接返回
        缓存的结果都有过期时间,过期后则再次爬去最新的内容
        知乎日报缓存3小时,微信公众号缓存1天
        '''
        html = self.redisDB.get(self.key)
        if html:
            print "====\tUse redisDB Data\t[%s]"%self.key
            self.set_header("Content-Type", "application/xml")
            self.finish(html)


        # 第一次生成后,永久存储,之后判断是否有
        # self.page_size = WEIXIN_PAGE_SIZE
        # if self.redisDB.hasKey(self.key):
        if self.key in get_list():
            self.page_size = 1
        else:
            self.page_size = WEIXIN_PAGE_SIZE


    def render(self, template_name, **kwargs):
        """Renders the template with the given arguments as the response."""
        html = self.render_string(template_name, **kwargs)

        # Insert the additional JS and CSS added by the modules on the page
        js_embed = []
        js_files = []
        css_embed = []
        css_files = []
        html_heads = []
        html_bodies = []
        for module in getattr(self, "_active_modules", {}).values():
            embed_part = module.embedded_javascript()
            if embed_part:
                js_embed.append(utf8(embed_part))
            file_part = module.javascript_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    js_files.append(file_part)
                else:
                    js_files.extend(file_part)
            embed_part = module.embedded_css()
            if embed_part:
                css_embed.append(utf8(embed_part))
            file_part = module.css_files()
            if file_part:
                if isinstance(file_part, (unicode_type, bytes)):
                    css_files.append(file_part)
                else:
                    css_files.extend(file_part)
            head_part = module.html_head()
            if head_part:
                html_heads.append(utf8(head_part))
            body_part = module.html_body()
            if body_part:
                html_bodies.append(utf8(body_part))

        def is_absolute(path):
            return any(path.startswith(x) for x in ["/", "http:", "https:"])
        if js_files:
            # Maintain order of JavaScript files given by modules
            paths = []
            unique_paths = set()
            for path in js_files:
                if not is_absolute(path):
                    path = self.static_url(path)
                if path not in unique_paths:
                    paths.append(path)
                    unique_paths.add(path)
            js = ''.join('<script src="' + escape.xhtml_escape(p) +
                         '" type="text/javascript"></script>'
                         for p in paths)
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + utf8(js) + b'\n' + html[sloc:]
        if js_embed:
            js = b'<script type="text/javascript">\n//<![CDATA[\n' + \
                b'\n'.join(js_embed) + b'\n//]]>\n</script>'
            sloc = html.rindex(b'</body>')
            html = html[:sloc] + js + b'\n' + html[sloc:]
        if css_files:
            paths = []
            unique_paths = set()
            for path in css_files:
                if not is_absolute(path):
                    path = self.static_url(path)
                if path not in unique_paths:
                    paths.append(path)
                    unique_paths.add(path)
            css = ''.join('<link href="' + escape.xhtml_escape(p) + '" '
                          'type="text/css" rel="stylesheet"/>'
                          for p in paths)
            hloc = html.index(b'</head>')
            html = html[:hloc] + utf8(css) + b'\n' + html[hloc:]
        if css_embed:
            css = b'<style type="text/css">\n' + b'\n'.join(css_embed) + \
                b'\n</style>'
            hloc = html.index(b'</head>')
            html = html[:hloc] + css + b'\n' + html[hloc:]
        if html_heads:
            hloc = html.index(b'</head>')
            html = html[:hloc] + b''.join(html_heads) + b'\n' + html[hloc:]
        if html_bodies:
            hloc = html.index(b'</body>')
            html = html[:hloc] + b''.join(html_bodies) + b'\n' + html[hloc:]

        # last work
        self.redisDB.set(self.key, html) # 缓存渲染的最终结果
        self.redisDB.expire(self.key, self.expires)
        print "++++	Cache [%s] to Redis Success ! ++++"%self.key
        # 存储feed list
        if update_feeds(self.key):
            print "++++	Update feeds [%s] Success ! ++++"%self.key
        # html=self.mc.get(self.key)
        self.finish(html)


class ZhihuBaseHandler(BaseHandler):

    def initialize(self):
        super(ZhihuBaseHandler, self).initialize()
        self.key = 'zhihu'
        self.expires = ZHIHU_EXPIRES



class jaqBaseHandler(BaseHandler):

    def initialize(self):
        super(jaqBaseHandler, self).initialize()
        self.key = self.request.uri[1:]
        self.expires = JAQ_EXPIRES



class WeixinBaseHandler(BaseHandler):

    def initialize(self):
        super(WeixinBaseHandler, self).initialize()
        # self.key = "wx__"+str(self.get_argument('id'))
        self.key = "wx__"+self.request.arguments['id'][0]
        self.expires = WEIXIN_EXPIRES