from denpendence import *
from setting import *

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
url1="http://www.jinyongwang.com/b/87055/3460556.html"
url2="http://www.jinyongwasda/b/87055/346asd6.html"
url3="http://www.jinyoadasdasd/87055/3460556.html"

 

""" pool = redis.ConnectionPool(decode_responses=True,host=redisInformation.host,db=redisInformation.db_ID,port=redisInformation.port)   #实现一个连接池
 
r = redis.Redis(connection_pool=pool) """

#clearRedis(redisHandel,hashname)
#clearMysql(mytool=mytool)
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

get50fromRedis(redisHandel,"bookitem")

""" import threading


def count1(num):
    print("123+",num,"={}".format(123+num))
    
def count2(num):
    print("666+",num,"={}".format(666+num))

num1=123
num2=333
t=threading.Thread(target=count1,args=(num1,))  #t为新创建的线程
t.start()
t2=threading.Thread(target=count2,args=(num2,))  #t为新创建的线程
t2.start() """
