# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from setting import *
from model import bookitem


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
        data=bookitem(bookname=bookname,authorname=authorname,chapternum=chapternum,content=content)
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

    
""" if __name__=='__main__':
    engine = create_engine('mysql+mysqlconnector://root:密码@localhost:3306/world')
    # 创建 DBSession 类型:
    DBSession = sessionmaker(bind=engine)
    # 创建 session 对象:
    session = DBSession()

    # 创建 Player 对象:
    new_player = Player(team_id=1101, player_name=" 约翰 - 雪诺 ", height=2.08)
    # 添加到 session:
    session.add(new_player)
    # 提交即保存到数据库:
    session.commit()
    session.close()
    # 查询身高 >=2.08 的球员有哪些
    rows_1 = session.query(Player).filter(Player.height >= 2.08).all()
    print([row.to_dict() for row in rows_1])

    rows_2 = session.query(Player).filter(or_(Player.height >=2.08, Player.height <=2.10)).all()
    print([row.to_dict() for row in rows_2])
    rows_3 = session.query(Player.team_id, func.count(Player.player_id)).group_by(Player.team_id).having(func.count(Player.player_id)>5).order_by(func.count(Player.player_id).asc()).all()
    print(rows_3)


    row = session.query(Player).filter(Player.player_name=='索恩-马克').first()
    row.height = 2.19
    session.commit()
    # 关闭 session:
    session.close()

    row = session.query(Player).filter(Player.player_name == ' 约翰 - 雪诺 ').first()
    session.delete(row)
    session.commit()
    session.close()
 """
