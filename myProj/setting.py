import redis

# 配置数据库信息，代理池，主从属性

# 项目属性配置
class projectInfo:
    ifmaster = 0
    masterIP = ""
    ifslave = 0
    slaveIP = ""



# redis数据库配置
class redisInformation():
    host = "192.168.112.143"
    port = 6379
    password = ""
    db_ID = 0
    


# 主从ip池
class master_slaves():
    masterIP = ""
    slavesIP_list = []


#数据存储数据库配置
class sqlInfo():
    host=""
    port=""
    password=""
    