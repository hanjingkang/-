#任务调度器

#每个url以（md5ID，url，status）的结构存储
#md5ID:用来去重
#url：原始信息
#status:是否分发执行（0:未分发 1:已分发 2:已结束）slave每完成一个url的爬取，返回redis一个请求，成功则将status置2,失败置0

def scheduler():
    print("读redis中的url,读各个slave中的负载情况,分配url任务")