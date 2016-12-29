# coding:utf-8

import json

from lxml import html as Xhtml
from lxml.etree import Element

from utils.date_format import zhihudate


def process_list(r):
    items = []

    rj=json.loads(r)
    date=rj['date']
    news=rj['news']
    for i in news:
        item = {}
        item['title'] = i['title']
        item['cover'] = i['image']
        item['link'] = i['share_url']
        item['json_url'] = i['url']
        item['created'] = zhihudate(date, i['ga_prefix'])
        item['guid'] = i['id']
        items.append(item)
    return items




def process_content(jsonBody,item_dict):
    entry = json.loads(jsonBody)
    content=Xhtml.fromstring(entry['body'])
    # get author
    # print item_dict['json_url']
    try:
        author=content.xpath('//span[@class="author"]/text()')[0].strip()
    except IndexError:
        author = ''
    try:
        bio=content.xpath('//span[@class="bio"]/text()')[0].strip()
    except IndexError:
        bio=''
    item_dict['author'] = author + bio

    coverelement = Element('img')
    coverelement.set('src', item_dict['cover'])
    content.insert(0, coverelement)

    item_dict['content'] = Xhtml.tostring(content, encoding='unicode')
    #
    print "++++\tGet zhihu items\t++++"
    print item_dict['cover']
    print item_dict['created']
    print item_dict['title']
    print item_dict['author']
    print item_dict['link']
    return item_dict