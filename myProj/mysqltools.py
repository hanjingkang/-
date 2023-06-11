# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from setting import *
from model import *


class mysqltools():
    def __init__(self,host,port,password,database,user):
        self.host=host
        self.port=port
        self.password=password
        self.database=database
        self.user=user
        self.DBsession=None
        self.session=None
        self.engine=None
    #连接数据库
    def connect(self):
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s'%
                               (self.user,self.password,self.host,self.port,self.database))
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        print("connect sucess")
        #Base.metadata.create_all(engine)
        self.DBsession=sessionmaker(bind=self.engine)
        #创建数据表
        try:
            bookitem.create(bind=self.engine)
            print("创建表")
        except:
            print("找到表")
    #打开会话
    def opensession(self):
        self.session=self.DBsession()
        print("open session")
    #添加book项 
    def addbook(self,bookname,authorname,chapternum,content):
        data=bookItem(bookname=bookname,authorname=authorname,chapternum=chapternum,content=content)
        self.session.add(data)
        print("add bookitem",bookname,"sucessful")
    #删除表
    def deleteTable(self):
         self.engine.execute(str('DROP TABLE IF EXISTS bookitem;'))
         print("delete bookitem ok")
    #提交会话
    def commitsession(self):
        self.session.commit()
        print("commit ok")
    #关闭会话 
    def closesession(self):
        self.session.close()
        print("close session")
 
mytool=mysqltools(host=MysqlInfo.host,port=MysqlInfo.port,
                  password=MysqlInfo.password,database=MysqlInfo.database,
                  user=MysqlInfo.user)



#item=bookItem(bookname="三体",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
""" mytool.connect()

mytool.opensession()
mytool.addbook(bookname="三体",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
mytool.commitsession()
mytool.closesession()
 """
    