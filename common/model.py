#! /usr/bin/env python
#coding=utf-8
from sqlalchemy import MetaData, Column, Integer, String, Float, CHAR
from sqlalchemy import DateTime, func, Unicode, UnicodeText, Boolean, Date, Text
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
#from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declared_attr
from datetime import *

Base = declarative_base()

class GPList(Base):

    __tablename__='gp_list'

    gid = Column(Integer, primary_key=True, autoincrement=False)
    title = Column(String(500), nullable=False, default='')
    user = Column(String(200), nullable=False, default='')
    comms = Column(Integer, nullable=False, default=0)
    clicks = Column(Integer, nullable=False, default=0)
    publish_date = Column(String(200), nullable=False, default='')
    updated_date = Column(String(200), nullable=False, default='')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class GPDetail(Base):

    __tablename__='gp_detail'

    gid = Column(Integer, primary_key=True, autoincrement=False)
    content = Column(UnicodeText, nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class GPComms(Base):

    __tablename__='gp_comms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False, default=0, index=True)
    content = Column(UnicodeText, nullable=False, default=u'')
    user = Column(Unicode(100), nullable=False, default=u'', index=True)
    #user = Column(String(200), nullable=False, default='', index=True)
    publish_date = Column(Unicode(50), nullable=False, default=u'', index=True)
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class StockList(Base):

    __tablename__='stock_list'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(UnicodeText, nullable=False, default=u'')
    url = Column(UnicodeText, nullable=False, default=u'')
    publish_time = Column(DateTime,nullable=False,default=datetime.now())
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class StockDetail(Base):

    __tablename__='stock_detail'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(UnicodeText, nullable=False, default=u'')
    content = Column(UnicodeText, nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class MeiShi(Base):

    __tablename__ = 'meishi'

    mid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, default=u'', index=True)
    url = Column(Unicode(50), nullable=False, default=u'')
    material = Column(Unicode(100), nullable=False, default=u'')
    author = Column(Unicode(50), nullable=False, default=u'')
    category = Column(Unicode(50), nullable=False, default=u'')
    source = Column(Unicode(50), nullable=False, default=u'')
    imgs = Column(UnicodeText, nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class LSLatLng(Base):

    __tablename__ = 'ls_latlng'

    rid = Column(Integer, primary_key=True, autoincrement=False)
    blat = Column(Unicode(50), nullable=False, default=u'')
    blng = Column(Unicode(50), nullable=False, default=u'')
    glat = Column(Unicode(50), nullable=False, default=u'')
    glng = Column(Unicode(50), nullable=False, default=u'')

class NMLatLng(Base):

    __tablename__ = 'nm_latlng'

    rid = Column(Integer, primary_key=True, autoincrement=False)
    blat = Column(Unicode(50), nullable=False, default=u'')
    blng = Column(Unicode(50), nullable=False, default=u'')
    glat = Column(Unicode(50), nullable=False, default=u'')
    glng = Column(Unicode(50), nullable=False, default=u'')

class NMMapping(Base):

    __tablename__ = 'nm_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Unicode(50), nullable=False, default=u'')
    nm_id = Column(Integer, nullable=False, default=0)
    nm_name = Column(Unicode(50), nullable=False, default=u'')
    nm_tel = Column(Unicode(50), nullable=False, default=u'')
    nm_addr = Column(Unicode(200), nullable=False, default=u'')
    gs_id = Column(Integer, nullable=False, default=0)
    gs_tel = Column(Unicode(50), nullable=False, default=u'')
    gs_name = Column(Unicode(50), nullable=False, default=u'')
    gs_addr = Column(Unicode(200), nullable=False, default=u'')
    distance = Column(Integer, nullable=False, default=0)
    similarity = Column(Float, nullable=False, default=0)


class MTMapping(Base):

    __tablename__ = 'mt_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Unicode(50), nullable=False, default=u'')
    mt_id = Column(Integer, nullable=False, default=0)
    mt_name = Column(Unicode(50), nullable=False, default=u'')
    mt_tel = Column(Unicode(50), nullable=False, default=u'')
    mt_addr = Column(Unicode(200), nullable=False, default=u'')
    gs_id = Column(Integer, nullable=False, default=0)
    gs_tel = Column(Unicode(50), nullable=False, default=u'')
    gs_name = Column(Unicode(50), nullable=False, default=u'')
    gs_addr = Column(Unicode(200), nullable=False, default=u'')
    distance = Column(Integer, nullable=False, default=0)
    similarity = Column(Float, nullable=False, default=0)
    is_api = Column(Boolean, nullable=False, default=False)

class MTMapping2(Base):

    __tablename__ = 'mt_mapping2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Unicode(50), nullable=False, default=u'')
    mt_id = Column(Integer, nullable=False, default=0)
    mt_name = Column(Unicode(50), nullable=False, default=u'')
    mt_tel = Column(Unicode(50), nullable=False, default=u'')
    mt_addr = Column(Unicode(200), nullable=False, default=u'')
    gs_id = Column(Integer, nullable=False, default=0)
    gs_tel = Column(Unicode(50), nullable=False, default=u'')
    gs_name = Column(Unicode(50), nullable=False, default=u'')
    gs_addr = Column(Unicode(200), nullable=False, default=u'')
    distance = Column(Integer, nullable=False, default=0)
    similarity = Column(Float, nullable=False, default=0)
    is_api = Column(Boolean, nullable=False, default=False)

class NMMapping2(Base):

    __tablename__ = 'nm_mapping2'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Unicode(50), nullable=False, default=u'')
    nm_id = Column(Integer, nullable=False, default=0)
    nm_name = Column(Unicode(50), nullable=False, default=u'')
    nm_tel = Column(Unicode(50), nullable=False, default=u'')
    nm_addr = Column(Unicode(200), nullable=False, default=u'')
    gs_id = Column(Integer, nullable=False, default=0)
    gs_tel = Column(Unicode(50), nullable=False, default=u'')
    gs_name = Column(Unicode(50), nullable=False, default=u'')
    gs_addr = Column(Unicode(200), nullable=False, default=u'')
    distance = Column(Integer, nullable=False, default=0)
    similarity = Column(Float, nullable=False, default=0)

class LSMapping(Base):

    __tablename__ = 'ls_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Unicode(50), nullable=False, default=u'')
    ls_id = Column(Unicode(50), nullable=False, default=u'')
    ls_name = Column(Unicode(50), nullable=False, default=u'')
    ls_tel = Column(Unicode(50), nullable=False, default=u'')
    ls_addr = Column(Unicode(200), nullable=False, default=u'')
    gs_id = Column(Integer, nullable=False, default=0)
    gs_tel = Column(Unicode(50), nullable=False, default=u'')
    gs_name = Column(Unicode(50), nullable=False, default=u'')
    gs_addr = Column(Unicode(200), nullable=False, default=u'')
    distance = Column(Integer, nullable=False, default=0)
    similarity = Column(Float, nullable=False, default=0)

class Student(Base):

    __tablename__ = 'student'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, default=u'')
    age = Column(Integer, nullable=False, default=0)
    sex = Column(Unicode(50), nullable=False, default=u'')

class Course(Base):

    __tablename__ = 'course'

    cid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, default=u'')
    t = Column(Integer, nullable=False, default=0)

class SC(Base):

    __tablename__ = 'score'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Integer, nullable=False, autoincrement=False)
    cid = Column(Integer, nullable=False, autoincrement=False)
    score = Column(Integer, nullable=False, autoincrement=False)

class Teacher(Base):

    __tablename__ = 'teacher'

    tid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, default=u'')

