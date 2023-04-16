# 所爬取数据的class类
from sqlalchemy import Column, String, Integer,Table,MetaData 
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.dialects.mysql import (INTEGER,CHAR,MEDIUMTEXT)
meta = MetaData()
bookitem=Table('bookitem',meta,
              Column('bookname',CHAR(50),primary_key=True),
              Column('authorname',CHAR(50)),
              Column('chapternum',INTEGER),
              Column('content',MEDIUMTEXT)
              )


Base = declarative_base()

#mysql数据表，存书的具体内容
class bookItem(Base):
    __tablename__ = 'bookitem'
    bookname = Column(String, primary_key=True, autoincrement=True)
    authorname = Column(String)
    chapternum = Column(Integer)
    content = Column(MEDIUMTEXT)
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    Base.to_dict = to_dict
