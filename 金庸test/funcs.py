# 主网址http://www.jinyongwang.com/
# book详情网址：主网址+/b/183674/
# 具体章节网址="/b/183674/913387.html"

import requests
from lxml import etree
import re
baseurl = "http://www.jinyongwang.com"
starturl = "http://www.jinyongwang.com/s/1/"
testbookurl="http://www.jinyongwang.com/b/87055/"
chaptertesturl="http://www.jinyongwang.com/b/87055/3460753.html"
testContenturl=""
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.42'
}


def gainBOOKurl(starturl, header):
    print("gainBOOKurl")
    page = requests.get(url=starturl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@class="w100"]')
    for i in range(0, len(part)):
        section = etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        bookurl = re.findall("<a href=(.*)><h2>.*</h2></a>", section)[0]
        bookname = re.findall("<a href=.*><h2>(.*)</h2></a>", section)[0]
        bookurl = baseurl+re.sub("\"", "", bookurl)
        print(bookname, bookurl)


def gainCHAPTERurl(bookurl):
    print("gainCHAPTERurl")
    page = requests.get(url=bookurl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@id="catalog"]//li')
    for i in range(0,len(part)):
        section=etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        chapterName=re.findall("<li><a href=.* title=.*>(.*)</a></li>",section)[0]
        chapterUrl=re.findall("<li><a href=(.*) title=.*>.*</a></li>",section)[0]
        chapterUrl=baseurl+re.sub("\"", "", chapterUrl)
        print(chapterName,chapterUrl)
    


def gainCONTENT(chapterurl):
    print("gainCONTENT")
    page = requests.get(url=chapterurl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//article[@id="article"]//p')
    chapterContent=""
    for i in range(0,len(part)):
         section=etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
         chapterContent+=section
    chapterContent=re.sub("</p>|<p>",'',chapterContent)
    return chapterContent
#gainBOOKurl(starturl, header)
#gainCHAPTERurl(testbookurl)
#print(gainCONTENT(chapterurl=chaptertesturl))

