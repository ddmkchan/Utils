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

class IQIYI_TV(Base):

    __tablename__ = 'iqiyi_tv'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tv_name = Column(String(50), nullable=False, default='')
    episode	= Column(String(50), nullable=False, default='')
    url = Column(String(200), nullable=False, default='')
    tvid = Column(Integer, nullable=False, default=0)
    qitanid = Column(Integer, nullable=False, default=0)


class IQIYI_TV_COMMENTS(Base):

    __tablename__ = 'iqiyi_tv_comments'

    comment_id = Column(String(50), primary_key=True)
    tv_name = Column(String(50), nullable=False, default='')
    episode	= Column(String(50), nullable=False, default='')
    comment = Column(Text, nullable=False, default='')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间



class LETV_TV_COMMENTS(Base):

    __tablename__ = 'letv_tv_comments'

    comment_id = Column(String(50), primary_key=True)
    tv_name = Column(String(50), nullable=False, default='')
    episode	= Column(String(50), nullable=False, default='')
    comment = Column(Text, nullable=False, default='')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class APPLIST(Base):

    __tablename__ = 'app_list'

    apkmd5 = Column(String(50), primary_key=True, autoincrement=False)
    app_name = Column(String(50), nullable=False, default=u'')
    category = Column(String(50), nullable=False, default=u'')
    campany_name = Column(String(100), nullable=False, default=u'')
    editor_info = Column(String(200), nullable=False, default=u'')
    source = Column(String(50), nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class APPLIST2(Base):

    __tablename__ = '360_list'

    sid = Column(Integer, primary_key=True, autoincrement=False)
    app_name = Column(String(50), nullable=False, default=u'')
    tags = Column(String(200), nullable=False, default=u'')
    category = Column(String(50), nullable=False, default=u'')
    app_type = Column(Integer, nullable=False, default=0)
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class BAIKEENTRY(Base):

    __tablename__ = 'baike_entry'

    query = Column(Unicode(50), primary_key=True, autoincrement=False)
    result = Column(Unicode(100), nullable=False, default=u'')
    url = Column(Unicode(100), nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间



class BAIKEDETAIL(Base):

    __tablename__ = 'baike_detail'

    query = Column(Unicode(50), primary_key=True, autoincrement=False)
    detail = Column(UnicodeText, nullable=False, default=u'')
    url = Column(Unicode(100), nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间


class BAIDUIPDATA(Base):

    __tablename__ = 'baidu_ip_data'

    ip = Column(String(50), primary_key=True, autoincrement=False)
    detail = Column(Text, nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间


class BAIDUIPDETAIL(Base):

    __tablename__ = 'baidu_ip_address'

    ip = Column(Unicode(50), primary_key=True, autoincrement=False)
    province = Column(Unicode(50), nullable=False, default=u'')
    city = Column(Unicode(50), nullable=False, default=u'')
    district = Column(Unicode(50), nullable=False, default=u'')
    street_number = Column(Unicode(50), nullable=False, default=u'')
    street = Column(Unicode(50), nullable=False, default=u'')
    city_code = Column(Integer, nullable=False, default=0)
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间


class KC(Base):

    __tablename__ = '9game_kc'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Unicode(50), nullable=False, default=u'')
    title = Column(Unicode(50), nullable=False, default=u'')
    title2 = Column(Unicode(50), nullable=False, default=u'')
    img = Column(Unicode(100), nullable=False, default=u'')
    url = Column(Unicode(100), nullable=False, default=u'')
    device = Column(Unicode(50), nullable=False, default=u'')
    status = Column(Unicode(50), nullable=False, default=u'')
    game_type = Column(Unicode(50), nullable=False, default=u'')
    popular = Column(Unicode(50), nullable=False, default=u'')
    kc_date = Column(Unicode(50), nullable=False, default=u'')
    create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
    last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间


class KC_LIST(Base):

	__tablename__ = 'kc_list'

	id = Column(Integer, primary_key=True, autoincrement=True)
	time = Column(Unicode(50), nullable=False, default=u'')
	title = Column(Unicode(50), nullable=False, default=u'')
	title2 = Column(Unicode(50), nullable=False, default=u'')
	img = Column(Unicode(100), nullable=False, default=u'')
	url = Column(Unicode(100), nullable=False, default=u'')
	device = Column(Unicode(50), nullable=False, default=u'')
	status = Column(Unicode(50), nullable=False, default=u'')
	game_type = Column(Unicode(50), nullable=False, default=u'')
	game_id = Column(Unicode(50), nullable=False, default=u'')
	pkg_name = Column(Unicode(100), nullable=False, default=u'')
	popular = Column(Unicode(50), nullable=False, default=u'')
	publish_date = Column(Unicode(50), nullable=False, default=u'')
	source = Column(Integer, nullable=False, default=0)
	create_date = Column(DateTime,nullable=False,default=datetime.now())#创建时间
	last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间

class HotGames(Base):
	
	__tablename__ = 'hot_games'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(Unicode(100), nullable=False, default=u'', index=True)
	src = Column(Unicode(200), nullable=False, default=u'')
	download_count = Column(Unicode(50), nullable=False, default=u'')
	size = Column(Unicode(100), nullable=False, default=u'')
	rank = Column(Integer, nullable=False, default=0)
	url = Column(Unicode(100), nullable=False, default=u'')
	status = Column(Unicode(50), nullable=False, default=u'')
	game_type = Column(Unicode(50), nullable=False, default=u'')
	popular = Column(Unicode(50), nullable=False, default=u'')
	source = Column(Integer, nullable=False, default=-1, index=True)
	create_date = Column(DateTime,nullable=False,default=date.today())#创建时间
	last_update = Column(DateTime,nullable=False,default=datetime.now())#最后更新时间


class PageSource(Base):
	
	__tablename__ = 'page_source'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	url = Column(Unicode(200), nullable=False, default=u'', index=True)
	code = Column(UnicodeText, nullable=False, default=u'')
	source = Column(Integer, nullable=False, default=-1, index=True)
	create_date = Column(DateTime,nullable=False,default=date.today())#创建时间
	last_update = Column(DateTime,nullable=False,default=date.today())#最后更新时间

class GameDetailByDay(Base):
	
	__tablename__ = 'game_detail_by_day'
	
	id = Column(Integer, primary_key=True, autoincrement=True)
	kc_id = Column(Integer, nullable=False, default=0, index=True)
	name = Column(Unicode(100), nullable=False, default=u'', index=True)
	imgs = Column(UnicodeText, nullable=False, default=u'')
	game_type = Column(Unicode(100), nullable=False, default=u'')
	summary = Column(UnicodeText, nullable=False, default=u'')
	download_num = Column(Unicode(50), nullable=False, default=u'')
	comment_num = Column(Unicode(50), nullable=False, default=u'')
	rating = Column(Unicode(50), nullable=False, default=u'')
	rank = Column(Unicode(50), nullable=False, default=u'')
	topic_num_day = Column(Unicode(50), nullable=False, default=u'')
	topic_num_total = Column(Unicode(50), nullable=False, default=u'')
	pkg_size = Column(Unicode(50), nullable=False, default=u'')
	company = Column(Unicode(100), nullable=False, default=u'')
	version = Column(Unicode(100), nullable=False, default=u'')
	author = Column(Unicode(100), nullable=False, default=u'')
	dt = Column(Unicode(100), nullable=False, default=u'')
	update_time = Column(Unicode(100), nullable=False, default=u'')
	create_date = Column(DateTime, nullable=False, default=datetime.now())#创建时间
	last_update = Column(DateTime, nullable=False, default=datetime.now())#最后更新时间

class Course(Base):

    __tablename__ = 'course'

    cid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(50), nullable=False, default=u'', info={'comment':'Segregation Code'})
    t = Column(Integer, nullable=False, default=0)



class ProxyList(Base):

	__tablename__ = 'proxy_list'

	id = Column(Integer, primary_key=True, autoincrement=True)
	ip = Column(Unicode(100), nullable=False, default=u'', index=True)
	port = Column(Unicode(20), nullable=False, default=u'', index=True)
	location = Column(Unicode(100), nullable=False, default=u'')
	is_anonymity = Column(Unicode(20), nullable=False, default=u'')
	type = Column(Unicode(20), nullable=False, default=u'')
	status = Column(Integer, nullable=False, default=0)
	check_time = Column(Unicode(100), nullable=False, default=u'')
	create_time = Column(DateTime, nullable=False, default=datetime.now())#创建时间
	last_update = Column(DateTime, nullable=False, default=datetime.now())#最后更新时间


