# coding:utf-8

from handlers import weibo, weixin_gs, zhihu, index,jaq,weixin,pediy,wx_mgt

urls=[
    (r"/", index.MainHandler),
    (r"/wx_mgt", wx_mgt.MainHandler),
    (r"/wx_mgt/del", wx_mgt.DelHandler),
    (r"/wx_mgt/add", wx_mgt.AddHandler),
    (r"/wx_mgt/group", wx_mgt.GroupHandler),
    (r"/wx_mgt/feeds", wx_mgt.FeedsHandler),
    (r"/weibo", weibo.WeiboHandler),
    (r"/weixin", weixin_gs.WeixinHandler),
    (r"/weixin_", weixin.WeixinHandler),
    # (r"/weixin_url_add", weixin_url_add.WeixinAddHandler),
    (r"/zhihu", zhihu.ZhihuHandler),
    (r"/jaq_tech", jaq.jaqHandler),
    (r"/jaq_news", jaq.jaqHandler),
    (r"/pediy", pediy.pediyHandler),
]