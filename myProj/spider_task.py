#定义具体爬虫任务
# 主网址http://www.jinyongwang.com/
# book详情网址：主网址+/b/183674/
# 具体章节网址="/b/183674/913387.html"

import requests
from lxml import etree
import re
from util import *
from denpendence import *
baseurl = "http://www.jinyongwang.com"
starturl = "http://www.jinyongwang.com/s/1/"
testbookurl="http://www.jinyongwang.com/b/87055/"
chaptertesturl="http://www.jinyongwang.com/b/87055/3460753.html"
testContenturl=""
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36 Edg/107.0.1418.42'
}
def cal_md5(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    print(md5_url)  # 2f7108ac307fd06f5995948f35a70f2f
    return md5_url
def pushinredis(key, value, redisHandle, hashname):
    if (redisHandle.hget(hashname, key)):
        print("key:", key, "already exits")
        return False
    else:
        redisHandle.hset(hashname, key, str(value))
        print("save key:", key)



#获取初始starturl，用来分配给slave
def gainStartUrl(starturl,slaveNums=3):
    print("gainStartUrl")
    page = requests.get(url=starturl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@class="pages"]')
    section = etree.tostring(part[0], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
    allcount = re.findall("&gt;&gt;</a><a href=.*>(.*)</a>", section)[0]
    reslist=[]
    for i in range(0,slaveNums):
        reslist.append(int((int(allcount)/slaveNums)*i+1))
    return reslist

#获取该索引页的所有bookurl，md5入库redis
def gainBOOKurl(indexurl, header=header):
    global redisHandel
    global hashname
    print("gainBOOKurl")
    page = requests.get(url=indexurl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@class="w100"]')
    for i in range(0, len(part)):
        section = etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        bookurl = re.findall("<a href=(.*)><h2>.*</h2></a>", section)[0]
        bookname = re.findall("<a href=.*><h2>(.*)</h2></a>", section)[0]
        authorname=re.findall("&nbsp;(.*)</i>", section)[0]
        bookurl = baseurl+re.sub("\"", "", bookurl)
        #print(bookname, bookurl)
        md5key=cal_md5(bookurl)
        value=bookname+"&&{}&&{}".format(authorname,bookurl)
        pushinredis(md5key,value,redisHandel,hashname)

#获取book页的所有chapterurl
def gainCHAPTERurl(bookurl):
    print("gainCHAPTERurl")
    page = requests.get(url=bookurl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@id="catalog"]//li')
    chapterList=[]
    for i in range(0,len(part)):
        section=etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        chapterName=re.findall("<li><a href=.* title=.*>(.*)</a></li>",section)[0]
        chapterUrl=re.findall("<li><a href=(.*) title=.*>.*</a></li>",section)[0]
        chapterUrl=baseurl+re.sub("\"", "", chapterUrl)
        chapterList.append([chapterName,chapterUrl])
        print(chapterName,chapterUrl)
    return chapterList

#获取章节内容
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

#接收master的start_url，将收集到的url发送到redis，set去重
def gainUrl(starturlnum):
    global closeflag
    print("收集url")
    baseurl = "http://www.jinyongwang.com/s/"
    start=int(starturlnum)
    while start<(int(starturlnum)+6000):
        gainBOOKurl(indexurl=(baseurl+str(start)+'/'),header=header)
        start+=1
        print("gain index:",start)
            
#接收来自调度器的bookurl，针对url执行爬取页面的操作,
def gainPage(url):
    print("收集page内容")
    chaplist=gainCHAPTERurl(url)
    contentlist=[]
    for i in chaplist:
        print("爬取 {}".format(i))
        content=[i[0],gainCONTENT(i[1])]
        contentlist.append(content)
    return contentlist
        
   