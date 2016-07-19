# coding:utf-8

from lxml import html as Xhtml
import lxml,re
from date_format import weixindate


def process_list(r):
    root = Xhtml.fromstring(r)
    list_len = len(root.xpath('//*[@class="article-ul"]/li'))
    out = []
    for i in range(1,list_len+1):
        o = {}
        o['img'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[1]/a/img')[0].attrib['data-hash']
        o['title'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/h4/a')[0].text
        o['desc'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/a')[0].text
        o['link'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/h4/a')[0].attrib['href']
        o['author'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/a/span')[0].text
        createDate = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/span[1]')[0].text[5:]
        o['created']=weixindate(createDate)
        o['book'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/font/text()[3]')[0].strip()
        o['up'] = root.xpath('//*[@class="article-ul"]/li['+str(i)+']/div[2]/div/font/text()[2]')[0].strip()
        out.append(o)
    return out




def process_content(html,item_dict):
    root = Xhtml.fromstring(html)

    # 抽取文章内容
    try:
        content = root.xpath('//*[@id="js_content"]')[0]
    except IndexError:
        return ''

    # 处理图片链接
    # leaf 3个视图:1rss内容;2自己从网页中提取的内容;3原始网页
    for img in content.xpath('.//img'):
        if not 'src' in img.attrib:
            img.attrib['src'] = img.attrib.get('data-src')

    # 抽取封面cover图片1,这个比gsdata封面清晰
    script = root.xpath('//*[@id="media"]/script/text()')
    _COVER_RE = re.compile(r'cover = "(http://.+)";')
    if script and _COVER_RE.findall(script[0]):
        item_dict['cover']= _COVER_RE.findall(script[0])[0]

    # 生成封面
    if item_dict['cover']:
        coverelement = lxml.etree.Element('img')
        coverelement.set('src', item_dict['cover'])
        content.insert(0, coverelement)

    # 生成HTML
    content=lxml.html.tostring(content, encoding='unicode')
    content = content[:content.rfind("<hr")]+"</div>"  # 清除垃圾
    item_dict['content'] = content

    #
    print "++++\tGet items\t++++"
    print item_dict['cover']
    print item_dict['created']
    print item_dict['title']
    print item_dict['desc']
    print item_dict['link']

    return item_dict