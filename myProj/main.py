from denpendence import *


#master端
if(projectInfo.ifmaster==1 and projectInfo.ifslave==0):
    print("master端")
    #server(master_slaves.masterIP,master_slaves.masterPort)
    mainservertask=threading.Thread(target=server,args=(master_slaves.masterIP,master_slaves.masterPort))
    dataservertask=threading.Thread(target=dataserver)
    mainservertask.start()
    dataservertask.start()

#slave端
elif(projectInfo.ifmaster==0 and projectInfo.ifslave==1):
    print("slave端")
    #开一个线程读系统性能
    #client(master_slaves.masterIP,master_slaves.masterPort)
    maintask=threading.Thread(target=client,args=(master_slaves.masterIP,master_slaves.masterPort))
    datatask=threading.Thread(target=dataclient)
    maintask.start()
    datatask.start()