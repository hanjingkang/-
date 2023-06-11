redis:放在master端:192.168.112.143 6379 nopassword
mysql：四个机子都有，端口统一为3306，密码Root_123，用户名root

mysql配置:https://blog.csdn.net/qq_44402184/article/details/122113037?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522167984141016800213030793%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=167984141016800213030793&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-122113037-null-null.142^v76^insert_down38,201^v4^add_ask,239^v2^insert_chatgpt&utm_term=centos%20mysql%E9%85%8D%E7%BD%AE&spm=1018.2226.3001.4187

安装py3

依赖：
redis
lxml
psutil--报错python.h:yum install python3-devel 
selenium
requests
pymysql
No module named 'sqlalchemy' 
    --python3 -m pip install --upgrade pip
    pip3 install gevent==1.4.0

lxml
sqlalchemy
sqlalchemy_utils

其他报错：
1
OSError: [Errno 113] No route to host
服务端关闭防火墙systemctl stop firewalld


mysql command：
设置数据包大小限制问题
etc/my.cnf添加：
max_allowed_packet=30M
重启sql

service mysqld restart
systemctl status mysqld