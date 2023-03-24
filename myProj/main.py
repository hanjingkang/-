from denpendence import *

if(projectInfo.ifmaster==1 and projectInfo.ifslave==0):
    print("执行调度器")
    do_schedeler()
    
elif(projectInfo.ifmaster==0 and projectInfo.ifslave==1):
    print("执行爬虫任务")
    do_spidertask()