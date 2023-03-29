from denpendence import *
from setting import redisInformation
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
url1="http://www.jinyongwang.com/b/87055/3460556.html"
url2="http://www.jinyongwasda/b/87055/346asd6.html"
url3="http://www.jinyoadasdasd/87055/3460556.html"

pool = redis.ConnectionPool(host=redisInformation.host,db=redisInformation.db_ID,port=redisInformation.port)   #实现一个连接池
 
r = redis.Redis(connection_pool=pool)

key1=cal_md5(url1)
key2=cal_md5(url2)
key3=cal_md5(url3)
r.hset("bookitem","init","init")
pushinredis(key1,url1,r,"bookitem")
pushinredis(key2,url2,r,"bookitem")
pushinredis(key3,url3,r,"bookitem")
pushinredis(key1,url1,r,"bookitem")



