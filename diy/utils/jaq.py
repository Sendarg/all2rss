# coding:utf-8

from lxml import html as Xhtml
from lxml.etree import Element

from configs import JAQ_ARTICLE


def process_list(r):
    root = Xhtml.fromstring(r)
    list_len = len(root.xpath('//*[@class="article-list"]/li'))
    out = []
    for i in range(1,list_len+1):
        o = {}
        o['author']=u'阿里聚安全@jaq.alibaba.com'
        o['title'] = root.xpath('//*[@class="article-list"]/li[%d]/h3/a'%i)[0].text.strip()
        o['desc'] = root.xpath('//*[@class="article-list"]/li[%d]/p[2]'%i)[0].text.strip()
        linkID = root.xpath('//*[@class="article-list"]/li[%d]/h3/a'%i)[0].attrib['href'].split("=")[1]
        o['link']= JAQ_ARTICLE.format(articleid=linkID)
        o['created'] = root.xpath('//*[@class="article-list"]/li[%d]/p[1]/text()[2]'%i)[0].strip()
        out.append(o)
    return out




def process_content(html,item_dict):
    root = Xhtml.fromstring(html)
    # 抽取文章内容
    try:
        content = root.xpath('//*[@class="article-content"]')[0]
    except IndexError:
        return ''
    #
    item_dict['cover'] = None
    imgs = root.xpath('//img[@src]')
    if imgs:
        for img in imgs:
            src=img.attrib['src'].strip()
            if src[-3:].lower() in ['jpg','png','gif'] :
                item_dict['cover']='http:'+src
                # 生成封面
                coverelement = Element('img')
                coverelement.set('src', item_dict['cover'])
                content.insert(0, coverelement)
            elif src[:22]=="data:image/png;base64,":
                img.set("src","")
            else:
                pass


    item_dict['content'] = Xhtml.tostring(content, encoding='unicode')
    #
    print "++++\tGet jaq items\t++++"
    print item_dict['cover']
    print item_dict['created']
    print item_dict['title']
    print item_dict['desc']
    print item_dict['link']
    return item_dict