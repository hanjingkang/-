#定义具体爬虫任务

#各个slave开一个线程，专门负责爬取url，可以从一个start_url开始，将收集到的url发送到redis，set去重
def gainUrl():
    print("收集url")

#各个salve开一个线程专门接收来自调度器的url，针对url执行爬取页面的操作,
def gainPage():
    print("收集page内容")