# coding:utf-8

from handlers import weibo, weixin_gs, zhihu, index,jaq,weixin_url_add,weixin,pediy

urls=[
    (r"/", index.MainHandler),
    (r"/weibo", weibo.WeiboHandler),
    (r"/weixin", weixin_gs.WeixinHandler),
    (r"/weixin_", weixin.WeixinHandler),
    (r"/weixin_url_add", weixin_url_add.WeixinAddHandler),
    (r"/zhihu", zhihu.ZhihuHandler),
    (r"/jaq_tech", jaq.jaqHandler),
    (r"/jaq_news", jaq.jaqHandler),
    (r"/pediy", pediy.pediyHandler),
]