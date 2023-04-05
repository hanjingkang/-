from hashlib import md5
import random
import os
import socket
import threading
import time
import psutil
import netifaces
from selenium import webdriver
import requests


def do_schedeler():
    print("do_schedeler")


def do_spidertask():
    print("do_spidertask")


def cal_md5(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    print(md5_url)  # 2f7108ac307fd06f5995948f35a70f2f
    return md5_url


def pushinredis(key, value, redisHandle, hashname):
    if(redisHandle.hget(hashname, key)):
        print("key:", key, "already exits")
        return False
    else:
        redisHandle.hset(hashname, key, str(value))
        print("save key:", key)


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
    load_average = os.getloadavg()

    # 获取磁盘利用率(百分之多少)
    disk_usage = psutil.disk_usage('/')

    # 获取内存利用率
    mem = psutil.virtual_memory()
    mem_percent = mem.percent

    # 获取网络连接状态
    net_connections = psutil.net_connections()
    for conn in net_connections:
        status = conn.status

    # 获取网络流量(接受)
    recv_before = psutil.net_io_counters().bytes_recv  # 已接收的流量
    time.sleep(1)
    recv_now = psutil.net_io_counters().bytes_recv
    recv = (recv_now - recv_before)

    # 系统性能打分：权重：disk*5+cpu*3+mem*2
    score = (1-disk_usage)*5+(1-cpu_percent) * 3+(1-mem_percent)*2

    # 打印结果
    """ print("CPU usage:", cpu_percent)
    print("load_average:", load_average)
    print("disk_usage:", disk_usage.percent)
    print("memory_usage:", mem_percent)
    print("net status", status)
    print("net recv speed:", recv) """
    print("sys score:", score)
    return score


#1.负责跟slave端交互，分发starturl和分配的url
#2.负责跟web交互，返回系统负载情况等
#3.接收与发送：接收值为1--开始信号，
# 发送starturl，delay(5s),发送分配的url，
# 接收3--（循环）发送sysScore，
# 接收4--接收sysScore,返回ok
def server_task(clientsock,buffsize,startNum):
    while True:  
        recvdata=clientsock.recv(buffsize).decode('utf-8')
        if recvdata=='1':
            print("start system")
            
        senddata=recvdata+'from sever'
        clientsock.send(senddata.encode())
    clientsock.close()



def server(host,port):
    HOST = host  
    PORT = port
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpSerSock = socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)  # 开始TCP监听,监听5个请求

    while True:
        clientsock,clientaddress=tcpSerSock.accept()
        print('connect from:',clientaddress)
        t=threading.Thread(target=server_task,args=(clientsock,BUFSIZ,startNum))  #t为新创建的线程
        t.start()
    tcpSerSock.close()













def client_task_send2redis(starturl):
    print("client线程之存url到redis,参数:starturl")

def client_task_acceptUrl(bookurl):
    print("client线程之接受调度url，存到mysql,参数:bookurl")



def client(host,port):
    HOST = host  # HOST 变量是空白的，表示它可以使用任何可用的地址。
    PORT = port
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    tcpCliSock = socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    tcpCliSock.send(bytes("client connected", 'utf-8'))
    while True:
        data = tcpCliSock.recv(BUFSIZ)
        #1.接收启动爬虫的启始地址 ,发送爬取的url到redis 3.接受master分配的url 
        # 5.接受查询（待定）6.结束
        if(data==1):
            starturl=data.decode('utf-8')
            t=threading.Thread(target=client_task_send2redis,args=(starturl))  #t为新创建的线程
            t.start()
            print("start url:",starturl)
        if(data==3):
            bookurl=data.decode('utf-8')
            t=threading.Thread(target=client_task_acceptUrl,args=(bookurl))  #t为新创建的线程
            t.start()
            print("process bookurl:",bookurl)

        
    tcpCliSock.close()




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
        if(self.method == 1):
            return self.ban_cookies()
        elif(self.method == 2):
            return self.random_agent()
        elif(self.method == 3):
            return self.add_Referer()
        elif(self.method == 4):
            return self.change_ip()


