from hashlib import md5

def do_schedeler():
    print("do_schedeler")
    
    
def do_spidertask():
    print("do_spidertask")
    

def cal_md5(url):
    md5_url = md5(url.encode('utf8')).hexdigest()
    print(md5_url)  # 2f7108ac307fd06f5995948f35a70f2f
    return md5_url
    

def pushinredis(key,value,redisHandle,hashname):
    if(redisHandle.hget(hashname,key)):
        print("key:",key,"already exits")
        return False
    else:
        redisHandle.hset(hashname,key,str(value))
        print("save key:",key)
    

    
    
""" 
以下是Python代码，使用了psutil和netifaces这两个第三方库：

import psutil
import netifaces

# 获取CPU利用率和负载
cpu_percent = psutil.cpu_percent(interval=1)
load_average = psutil.getloadavg()

# 获取磁盘I/O负载、利用率和inode利用率
disk_io = psutil.disk_io_counters()
disk_usage = psutil.disk_usage('/')
inode_usage = psutil.disk_usage('/').percent

# 获取内存利用率
mem = psutil.virtual_memory()
mem_percent = mem.percent

# 获取网络连接状态
net_connections = psutil.net_connections()
for conn in net_connections:
    status = conn.status

# 获取网络流量
net_ifaces = netifaces.interfaces()
for iface in net_ifaces:
    addrs = netifaces.ifaddresses(iface)
    if netifaces.AF_INET in addrs.keys():
        rx_bytes = addrs[netifaces.AF_INET][0]['rxbytes']
        tx_bytes = addrs[netifaces.AF_INET][0]['txbytes']

# 打印结果
print("CPU利用率：", cpu_percent)
print("负载：", load_average)
print("硬盘I/O负载：", disk_io)
print("硬盘利用率：", disk_usage.percent)
print("硬盘inode利用率：", inode_usage)
print("内存利用率：", mem_percent)
print("网络连接状态：", status)
print("网络流量（接收）：", rx_bytes)
print("网络流量（发送）：", tx_bytes)




"""




""" 
好的，下面是一个可以评估系统性能分数的Python函数：

```python
import psutil
import netifaces

def evaluate_system_performance():
    # 获取CPU利用率和负载
    cpu_percent = psutil.cpu_percent(interval=1)
    load_average = psutil.getloadavg()
    
    # 获取磁盘I/O负载、利用率和inode利用率
    disk_io = psutil.disk_io_counters()
    disk_usage = psutil.disk_usage('/')
    inode_usage = psutil.disk_usage('/').percent
    
    # 获取内存利用率
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    
    # 获取网络连接状态
    net_connections = psutil.net_connections()
    for conn in net_connections:
        status = conn.status
    
    # 获取网络流量
    net_ifaces = netifaces.interfaces()
    for iface in net_ifaces:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs.keys():
            rx_bytes = addrs[netifaces.AF_INET][0]['rxbytes']
            tx_bytes = addrs[netifaces.AF_INET][0]['txbytes']
    
    # 计算性能分数
    score = 100
    if cpu_percent > 80:
        score -= 20
    elif cpu_percent > 60:
        score -= 10
        
    if load_average[0] > 2.0:
        score -= 20
    elif load_average[0] > 1.0:
        score -= 10
        
    if disk_io.read_count > 100 or disk_io.write_count > 100:
        score -= 20
        
    if disk_usage.percent > 80:
        score -= 20
    elif disk_usage.percent > 60:
        score -= 10
    
    if inode_usage > 80:
        score -= 20
    elif inode_usage > 60:
        score -= 10
    
    if mem_percent > 80:
        score -= 20
    elif mem_percent > 60:
        score -= 10
    
    if status != 'ESTABLISHED':
        score -= 10
        
    if rx_bytes < 1000000 or tx_bytes < 1000000:
        score -= 10
    
    return max(score, 0)
```

这个函数会返回一个0到100之间的分数，分数越高代表系统性能越好，分数越低代表系统性能越差。函数首先获取各项性能指标，然后计算分数。对于每个指标，如果它的值超过一定阈值，则减去一定分数。最终，我们返回计算出来的得分。


"""