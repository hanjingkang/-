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
        
    def connect(self):
        engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s'%
                               (self.user,self.password,self.host,self.port,self.database))
        if not database_exists(engine.url):
            create_database(engine.url)
        print("connect sucess")
        #Base.metadata.create_all(engine)
        self.DBsession=sessionmaker(bind=engine)
        #创建数据表
        try:
            bookitem.create(bind=engine)
            print("创建表")
        except:
            print("找到表")
        

    def opensession(self):
        self.session=self.DBsession()
        print("open session")
        
    def addbook(self,bookname,authorname,chapternum,content):
        data=bookItem(bookname=bookname,authorname=authorname,chapternum=chapternum,content=content)
        self.session.add(data)
        print("add bookitem",bookname,"sucessful")
        
    def commitsession(self):
        self.session.commit()
        print("commit ok")
    
    def closesession(self):
        self.session.close()
        print("close session")
        
mytool=mysqltools(host=MysqlInfo.host,port=MysqlInfo.port,
                  password=MysqlInfo.password,database=MysqlInfo.database,
                  user=MysqlInfo.user)
#item=bookItem(bookname="三体",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
mytool.connect()

mytool.opensession()
mytool.addbook(bookname="三体",authorname="刘慈欣",chapternum=333,content="三体人入侵地球")
mytool.commitsession()
mytool.closesession()

    