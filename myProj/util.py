from hashlib import md5
import random
import os
import socket
import threading
import time
import psutil
from selenium import webdriver
import requests
from spider_task import *
from mysqltools import *

clientList = []
#格式：score, cpu_percent, disk_usage, mem_percent, recv
syscore = [[0,0,0,0,0], [0,0,0,0,0],[0,0,0,0,0]]

urlfinishflag=[]


def findUrl2Slave(clientsockt):
    global redisHandel
    global hashname
    res = get50fromRedis(redisHandel, hashname,5)  
    clientsockt.send(("2,"+str(res)).encode())
    print("send 50 url ok")


def do_schedeler():
    global syscore
    global clientList
    while True:
        time.sleep(30)
        # 循环获取slave的sysscore
        print("do_schedeler")
        # 计算最空闲slave
        s1, s2, s3 = syscore[0][0], syscore[1][0], syscore[2][0]
        target = max(s1, max(s2, s3))
        if (target == s1):
            # 向slave1分发50个url
            print("choose slave1")
            findUrl2Slave(clientList[0])
        elif (target == s2):
            # 向slave2分发50个url
            print("choose slave2")
            findUrl2Slave(clientList[1])
        elif (target == s3):
            # 向slave3分发50个url
            print("choose slave3")
            findUrl2Slave(clientList[2])
        


def do_spidertask(clientsoket, startnum):
    global urlfinishflag
    print("do_spidertask:", startnum)
    clientsoket.send(("1,"+str(startnum)).encode())
    data=clientsoket.recv(1024).decode('utf-8')
    print(data)
    urlfinishflag.append(1)
    
    


def cal_md5(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    print(md5_url)  # 2f7108ac307fd06f5995948f35a70f2f
    return md5_url


def clearRedis(redisHandle, hashname):
    print("clear redis")
    v = redisHandle.hgetall(hashname)
    if (len(v) == 0):
        print("redis empty")
        return 0
    for part in v:
        res = redisHandle.hdel(hashname, part)
        print("delete:", part[0], "成功"if (res == 1)else "失败")
    print("clear redis sucessful")


def clearMysql(mytool):
    print("clearMysql")
    mytool.connect()
    mytool.deleteTable()


def get50fromRedis(redisHandle, hashname,partsize):
    print("get 50urls from redis")
    v = redisHandle.hkeys(hashname)
    temp = None
    urllist = []
    if (len(v) == 0):
        print("redis empty")
        return None
    elif (len(v) < partsize):
        print("redis less then 50")
        temp = v
    else:
        print("redis more then 50")
        temp = v[:partsize]
    for part in temp:
        url = redisHandle.hget(hashname, part)
        urllist.append(url)
        res = redisHandle.hdel(hashname, part)
        print("get url:", url, "成功"if (res == 1)else "失败")
    print("get 50urls done")
    return urllist


def pushinredis(key, value, redisHandle, hashname):
    if (redisHandle.hget(hashname, key)):
        print("key:", key, "already exits")
        return False
    else:
        redisHandle.hset(hashname, key, str(value))
        print("save key:", key)


def pushinMysql(mytool, bookname, authorname, chapternum, content):
    mytool.connect()
    mytool.opensession()
    mytool.addbook(bookname=bookname, authorname=authorname,
                   chapternum=chapternum, content=content)
    mytool.commitsession()
    mytool.closesession()


def cal_sysLoad():
    #!/usr/bin/python
    # -*- coding: utf-8 -*
    """ ('CPU usage:', 3.1)
    ('load_average:', (0.04, 0.17, 0.21))
    ('disk_usage:', 65.3)
    ('memory_usage:', 94.8)
    ('net status', 'ESTABLISHED')
    ('net recv speed:', 120) """

    # 获取CPU利用率和负载
    cpu_percent = psutil.cpu_percent(interval=1)
    # load_average = os.getloadavg()

    # 获取磁盘利用率(百分之多少)
    disk_usage = psutil.disk_usage('/').percent

    # 获取内存利用率
    mem = psutil.virtual_memory()
    mem_percent = mem.percent


    # 获取网络流量(接受)
    recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
    time.sleep(1)
    recv_now = psutil.net_io_counters().bytes_recv
    recv = (recv_now - recv_before)

    # 系统性能打分：权重：disk*5+cpu*3+mem*2
    score = (1-float(disk_usage)*0.01)*5+(1-float(cpu_percent)*0.01) * 3+(1-float(mem_percent)*0.01)*2

    # 打印结果
    """ print("CPU usage:", cpu_percent)
    print("load_average:", load_average)
    print("disk_usage:", disk_usage.percent)
    print("memory_usage:", mem_percent)
    print("net status", status)
    print("net recv speed:", recv) """
    # print("sys score:", score)
    return [score, cpu_percent, disk_usage, mem_percent, float(recv/1024)]


# 1.负责跟slave端交互，分发starturl和分配的url
# 2.负责跟web交互，返回系统负载情况等
# 3.接收与发送：接收值为1--开始信号，
# 发送starturl，delay(5s),发送分配的url，
# 接收3--（循环）发送sysScore，
# 接收4--接收sysScore,返回ok

def server_task(clientsock, buffsize):
    global clientList
    global syscore
    global redisHandel
    global hashname
    global urlfinishflag
    while True:
        recvdata = clientsock.recv(buffsize).decode('utf-8')
        # 1.开启爬虫
        if recvdata == '1':
            print("web call:start system")
            clientsock.send(("start system sucessful!").encode())
            t1 = threading.Thread(target=findUrl2Slave,args=(clientList[0],)) 
            t2 = threading.Thread(target=findUrl2Slave,args=(clientList[1],)) 
            t3 = threading.Thread(target=findUrl2Slave,args=(clientList[2],)) 
            t1.start()
            time.sleep(5)
            t2.start()
            time.sleep(5)
            t3.start()

            do_schedeler()
        # 2.测试连接
        if recvdata == '2':
            print("web call:test connection")
            clientsock.send(("connect sucessful!").encode())
        # 3 接收sysscore
        if recvdata == '3':
            # targetclient=clientList[0]
            # targetclient.send(("3,").encode())
            # print("send 3")
            # scorestr= targetclient.recv(buffsize).decode('utf-8')
            # print("recv 3:",scorestr)
            # [[CPU_usage * 3], [netspeed * 3], [memory_usage * 3], [redis * 1], [disk_usage * 3]]
            res =[]
            res.extend([syscore[0][1],syscore[1][1],syscore[2][1]])
            res.extend([syscore[0][4],syscore[1][4],syscore[2][4]])
            res.extend([syscore[0][3],syscore[1][3],syscore[2][3]])
            res.extend([redisHandel.hlen(hashname),syscore[0][2],syscore[1][2],syscore[2][2]])
            print(res)
            # res=testdata()
            clientsock.send(str(res).encode())
        #5.收集url
        if recvdata == "5":
            print("web call:do url gain")
            starturllist = gainStartUrl(starturl)
            print(starturllist)
            # # 分发url
            t1 = threading.Thread(target=do_spidertask, args=(
                clientList[0], starturllist[0]))  # t为新创建的线程
            t2 = threading.Thread(target=do_spidertask, args=(
                clientList[1], starturllist[1]))
            t3 = threading.Thread(target=do_spidertask, args=(
                clientList[2], starturllist[2]))
            # do schedeler and get sysscore
            t1.start()
            t2.start()
            t3.start()
            clientsock.send("正在爬取url".encode())
        #6.检查状态
        if recvdata == "6":
            clientsock.send(str(redisHandel.hlen(hashname)).encode())
        #q是reset,清除数据库
        if recvdata == "q":
            clearRedis(redisHandel,hashname)
            print("client close")
            clientList[0].send(("4,").encode())
            #clientList[1].send(("4,").encode())
            #clientList[2].send(("4,").encode())
            clientsock.send(("reset sucessful!,close").encode())
            break
        #7.停止爬虫
        if recvdata == "7":
            print("web call:stop spider task")
            clientList[0].send(("5,").encode())
            #clientList[1].send(("5,").encode())
            #clientList[2].send(("5,").encode())
            clientsock.send(("stop spider task ok").encode()) 
    clientsock.close()


def server(host, port):
    HOST = host
    PORT = port
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)  # 开始TCP监听,监听5个请求
    global clientList
    print("master turn on")
    while True:
        clientsock, clientaddress = tcpSerSock.accept()
        clientList.append(clientsock)  # 前三个client是slave端,最后一个client是web端
        #print('connect from:', clientaddress)
        t = threading.Thread(target=server_task, args=(
            clientsock, BUFSIZ))  # t为新创建的线程
        t.start()
    tcpSerSock.close()


def client_task_send2redis(startnum,servsock):
    print("client线程之存url到redis,参数:starturl")
    gainUrl(startnum)
    servsock.send(bytes("gain url ok", 'utf-8'))
    print ("get all url ok ,then call server")




def client_task_acceptUrl(bookurllist):
    global mytool
    global closeflag
    print("client线程之接受调度url,存数据存到mysql,参数:bookurllist")
    for item in bookurllist:
        bookname=item.split("&&")[0]
        authorname="zuozhe"
        url=item.split("&&")[1]
        if(closeflag==False):
            contentlist = gainPage(url)
            print("爬完：",bookname,"一共{}章".format(len(contentlist)))
            pushinMysql(mytool, bookname,authorname, len(contentlist), str(contentlist))
            print("save book {} ok".format(bookname))
        else:
            print("task already closed")


def client(host, port):
    global mytool
    global closeflag
    HOST = host  # HOST 变量是空白的，表示它可以使用任何可用的地址。
    PORT = port
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        data = tcpCliSock.recv(5000)
        print("recv {} from server".format(data))
        data = data.decode('utf-8').split(",",1)
        # 1.接收启动爬虫的启始地址 ,发送爬取的url到redis
        if (data[0] == "1"):
            closeflag=False
            startnum = data[1]
            t = threading.Thread(
                target=client_task_send2redis, args=(startnum,tcpCliSock))  # t为新创建的线程
            t.start()
            print("start num:", startnum)
        # 2.接受master分配的url
        if (data[0] == "2"):
            closeflag=False
            urllist = ast.literal_eval(data[1])
            t = threading.Thread(target=client_task_acceptUrl,
                                 args=(urllist,))  # t为新创建的线程
            t.start()
            print("process bookurl:", urllist)
        # 3.发送sysscore
        if (data[0] == "3"):
            res = cal_sysLoad()
            print("cal_sysLoad:", res)
            tcpCliSock.send(bytes(str(res), 'utf-8'))
            print("send ok")
        #4.清理数据库
        if (data[0] == "4"):
            clearMysql(mytool)
            closeflag=False
            print("clearMysql ok")
        #5.停止爬虫
        if (data[0] == "5"):
            closeflag=True
            print("stop task ok")
            


class AAntispider():
    def __init__(self, method, url):
        self.method = method
        self.url = url

    def ban_cookies(self):
        browser = webdriver.Chrome()
        browser.get(self.url)
        browser.delete_all_cookies()
        return 1

    def random_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
        ]

        headers = {
            'User-Agent': random.choice(user_agents),
        }

        response = requests.get(self.url, headers=headers)
        return response

    def add_Referer(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
        ]
        headers = {
            'User-Agent': random.choice(user_agents),
            'Referer': self.url,
        }

        response = requests.get(self.url, headers=headers)
        return response

    def change_ip(self):
        proxies = {
            'http': 'http://10.10.1.10:3128',
            'https': 'https://10.10.1.10:1080',
        }

        response = requests.get(self.url, proxies=proxies)
        return response

    # method:1==禁用cookies,2==随机user_agent,3==#添加Referer,4==#换IP
    def process(self):
        if (self.method == 1):
            return self.ban_cookies()
        elif (self.method == 2):
            return self.random_agent()
        elif (self.method == 3):
            return self.add_Referer()
        elif (self.method == 4):
            return self.change_ip()


def testdata():
    res=[]
    for i in range(0, 4):
        res.append(random.randrange(1, 100))
        res.append(random.randrange(1, 100))
        res.append(random.randrange(1, 100))
    res.append(random.randrange(1, 10))
    for i in range(0, 3):
        res.append(random.randrange(1, 100))
    return res


def task(clientsock,i):
    global syscore
    while True:
        clientsock.send(("ask for s{} score".format(i)).encode())
        data1=str(clientsock.recv(1024).decode('utf-8'))
        #print("recv s{} score".format(i))
        data1=data1.replace("[","").replace("]","").replace(" ","").split(",")
        for j in range(len(data1)):
            data1[j]=float(data1[j])
        syscore[i]=data1
        #print(syscore[i])
        time.sleep(3)


def dataserver():
    
    HOST = "192.168.112.143"  # HOST 变量是空白的，表示它可以使用任何可用的地址。
    PORT = 8001
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    tcpSerSock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)  # 开始TCP监听,监听5个请求
    print("master turn on")
    i=0
    while True:
        clientsock, clientaddress = tcpSerSock.accept()
        t=threading.Thread(target=task,args=(clientsock,i))
        t.start()
        i+=1
        print('connect and from:', clientaddress)
        
    tcpSerSock.close()


def dataclient():
    HOST = "192.168.112.143"  # HOST 变量是空白的，表示它可以使用任何可用的地址。
    PORT = 8001
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        data=tcpCliSock.recv(1024)
        #print(data)
        res = cal_sysLoad()
        # print("cal_sysLoad:", res)
        tcpCliSock.send(bytes(str(res), 'utf-8'))
        #print("send ok")
