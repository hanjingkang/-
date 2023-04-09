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
#获取初始urlnum，用来分配给slave
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
    print("gainBOOKurl")
    page = requests.get(url=indexurl, headers=header)
    html = etree.HTML(page.text)
    part = html.xpath('//div[@class="w100"]')
    for i in range(0, len(part)):
        section = etree.tostring(part[i], encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
        bookurl = re.findall("<a href=(.*)><h2>.*</h2></a>", section)[0]
        bookname = re.findall("<a href=.*><h2>(.*)</h2></a>", section)[0]
        bookurl = baseurl+re.sub("\"", "", bookurl)
        print(bookname, bookurl)
        md5key=cal_md5(bookurl)
        value=bookname+"[{}]".format(bookurl)
        pushinredis(md5key,value,redisHandel,hashname)



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
#print(gainStartUrl(starturl))



#各个slave开一个线程，专门负责爬取url，可以从一个start_url开始，将收集到的url发送到redis，set去重
def gainUrl(starturlnum):
    print("收集url")
    baseurl = "http://www.jinyongwang.com/s/"
    start=starturlnum
    while start<30000:
        gainBOOKurl(indexurl=(baseurl+start+'/'),header=header)
        start+=1
        print("gain index:",start)
        
        
    

#各个salve开一个线程专门接收来自调度器的url，针对url执行爬取页面的操作,
def gainPage(url,bookname):
    print("收集page内容")
    chaplist=gainCHAPTERurl(url)
    contentlist=[]
    for i in chaplist:
        content=[i[0],gainCONTENT(i[1])]
        contentlist.append(content)
    return bookname,contentlist
        
   