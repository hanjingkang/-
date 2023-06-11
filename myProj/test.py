from denpendence import *
from setting import *
from util import *
'''
这种连接是连接一次就断了，耗资源.端口默认6379，就不用写
r = redis.Redis(host='127.0.0.1',port=6379,password='tianxuroot')
r.set('name','root')
print(r.get('name').decode('utf8'))
'''
'''
连接池：
当程序创建数据源实例时，系统会一次性创建多个数据库连接，并把这些数据库连接保存在连接池中，当程序需要进行数据库访问时，
无需重新新建数据库连接，而是从连接池中取出一个空闲的数据库连接
'''
url1 = "http://www.jinyongwang.com/b/87055/3460556.html"
url2 = "http://www.jinyongwasda/b/87055/346asd6.html"
url3 = "http://www.jinyoadasdasd/87055/3460556.html"


""" pool = redis.ConnectionPool(decode_responses=True,host=redisInformation.host,db=redisInformation.db_ID,port=redisInformation.port)   #实现一个连接池

r = redis.Redis(connection_pool=pool) """

# clearRedis(redisHandel,hashname)
# clearMysql(mytool=mytool)
""" pushinMysql(mytool=mytool,bookname="三体2",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
pushinMysql(mytool=mytool,bookname="三体3",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
pushinMysql(mytool=mytool,bookname="三体4",authorname="刘慈欣",chapternum=333,content="三体人入侵地球") """

""" key1=cal_md5(url1)
key2=cal_md5(url2)
key3=cal_md5(url3)
r=redisHandel
r.hset("bookitem","init","init")
pushinredis(key1,url1,r,"bookitem")
pushinredis(key2,url2,r,"bookitem")
pushinredis(key3,url3,r,"bookitem")
pushinredis(key1,url1,r,"bookitem") """

#get50fromRedis(redisHandel, "bookitem")



HOST = "192.168.112.143"  # HOST 变量是空白的，表示它可以使用任何可用的地址。
PORT = 8000
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect(ADDR)
while True:
    data=tcpCliSock.recv(1024)
    print(data)
    res = cal_sysLoad()
    print("cal_sysLoad:", res)
    tcpCliSock.send(bytes(str(res), 'utf-8'))
    print("send ok")
    

    # while True:
    #     data = tcpCliSock.recv(BUFSIZ)
    #     print("recv {} from server".format(data))
    #     data = data.decode('utf-8').split(",")

    #     # 5.接受查询（待定）6.结束

    #     # 1.接收启动爬虫的启始地址 ,发送爬取的url到redis
    #     if (data[0] == "1"):
    #         startnum = data[1]
    #         t = threading.Thread(
    #             target=client_task_send2redis, args=(startnum))  # t为新创建的线程
    #         t.start()
    #         print("start num:", startnum)
    #     # 2.接受master分配的url
    #     if (data[0] == "2"):
    #         urllist = data[1]
    #         t = threading.Thread(target=client_task_acceptUrl,
    #                              args=(urllist))  # t为新创建的线程
    #         t.start()
    #         print("process bookurl:", urllist)
    #     # 3.发送sysscore
    #     if (data[0] == "3"):
    #         res = cal_sysLoad()
    #         print("cal_sysLoad:", res)
    #         tcpCliSock.send(bytes(str(res), 'utf-8'))
    #         print("send ok")
