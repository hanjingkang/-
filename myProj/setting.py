import redis

# 配置数据库信息，代理池，主从属性

# 项目属性配置
class projectInfo:
    ifmaster = 1
    masterIP = "192.168.112.143"
    ifslave = 0
    slaveIP = ""



# redis数据库配置
class redisInformation():
    host = "192.168.112.143"
    port = 6379
    password = ""
    db_ID = 0

pool = redis.ConnectionPool(host=redisInformation.host,db=redisInformation.db_ID,port=redisInformation.port,decode_responses=True)   #实现一个连接池
redisHandel = redis.Redis(connection_pool=pool)
hashname="bookitem"


# 主从ip池
class master_slaves():
    masterIP = "192.168.112.143"
    masterPort=8000
    slavesIP_list = ["192.168.112.3","192.168.112.4","192.168.112.5"]
    slavesPort_list=[8000,8000,8000]


#数据存储数据库配置
class MysqlInfo():
    host="192.168.112.143"
    port="3306"
    password="Root_123"
    user="root"
    database="testdb"
    