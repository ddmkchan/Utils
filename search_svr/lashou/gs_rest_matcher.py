#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import sys
sys.path.append("/home/chenyp/Utils")
sys.path.append("../")
import traceback
from common.logger import *
from common.model import NMLatLng
from common.define import session as ptpq_session
from define import session
import xlrd
import xlwt
from gs_rest_searcher import *
from convert_coords import convert_baidu_coords
    
_log = get_logger("rest_match")

def get_city_mapping():
    mydict = {}
    f = open("ls_city_mapping")
    for l in f.readlines():
        segs = l.rstrip().split()
        mydict[segs[0].decode('utf-8')] = segs[1]
    f.close()
    return mydict

def get_city_url_to_gs():
    name_to_gs = get_city_mapping()
    mydict = {}
    for r in session.execute("select * from city_ls"):
        cname = r[1]
        url = r[2]
        gs_id = name_to_gs.get(cname, '')
        if gs_id:
            mydict[url] = gs_id
    return mydict
        

def phone_match(s1, s2):
    s2 = re.sub('\s+', '', s2)
    s1 = re.sub('\s+', '', s1)
    if len(s1)>0 and len(s2)>0 and (s1 in s2 or s2 in s1):
        return True
    return False

def address_match(s1, s2):
    if not isinstance(s1, unicode):
        s1 = re.sub(u'\s+', u'', s1.decode('utf-8'))
    if not isinstance(s2, unicode):
        s2 = re.sub(u'\s+', u'', s2.decode('utf-8'))
    if len(s1) > 0 and len(s2) > 0:
        addr_sim =  cosine_similarity(s1, s2)
        return addr_sim
    return 0

def rest_search():
    city_mapping = get_city_url_to_gs()
    for r in session.execute("select name, address, lat, lng, url, phone, id from restaurant_ls_merge limit 10000"):
        rid = r[6]
        name = r[0]
        ls_addr = r[1]
        blat = r[2]
        blng = r[3]
        url = r[4]
        ls_tel = r[5]
        glat = 0
        glom = 0
        if blat is not None:
            latlng = ptpq_session.execute("select glat, glng from ls_latlng where rid= %s" % rid).first()
            if latlng is not None:
                glat = float(latlng[0])
                glon = float(latlng[1])
        if u"html" in url:
            _id = re.split(u"\/|\.", url)[-2]
        else:
            _id = re.split(u"\/|\.", url)[-1]
        ismatched = False
        city_url = re.split(u'\\/s', url)[0]
        gs_distirct_id = city_mapping.get(city_url, 0)
        #print city_url, name, gs_distirct_id
        if gs_distirct_id != 0:
            rs = search_poi(keyword=name, district_id=gs_distirct_id, length=5)
            if rs['total'] > 0:
                for ret in rs['data']:
                    tel = re.sub('\s+', u'', ret['tel'])
                    addr = re.sub('\s+', u'', ret['address'])
                    if not isinstance(tel, unicode):
                        tel = tel.decode('utf-8')
                    distance = -1
                    r_lat, r_lon = float(ret['lat']), float(ret['lon'])
                    if (glat != 0 or glon != 0) and (r_lat !=0 or r_lon !=0):
                        distance = get_distance(glat, glon, r_lat, r_lon)
                    try:
                        if ret['Levenshtein_ratio'] >= 0.8:
                            if phone_match(ls_tel, tel):
                                ismatched = True
                                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("高度匹配电话相同", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                            elif address_match(addr, ls_addr) >= 0.6:
                                ismatched = True
                                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("高度匹配地址部分匹配", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                            elif distance > 0 and distance < 1000:
                                ismatched = True
                                print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("高度匹配距离较近", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                            else:
                                if not ismatched:
                                    ismatched = True
                                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("仅高度匹配", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                        else:
                            if ret['Levenshtein_ratio'] >= 0.6:
                                if phone_match(ls_tel, tel) and not ismatched:
                                    ismatched = True
                                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("部分匹配电话相同", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                                elif address_match(addr, ls_addr) >= 0.6 and not ismatched:
                                    ismatched = True
                                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("部分匹配地址部分匹配", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                                elif distance > 0 and distance < 1000 and not ismatched:
                                    ismatched = True
                                    print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("部分匹配距离较近", _id.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'), ret['id'], ret['name'].encode('utf-8'), tel.encode('utf-8'), addr.encode('utf-8'), distance, ret['Levenshtein_ratio'])
                    except Exception,e:
                        _log.error("%s\t%s" % (url, name))
                if not ismatched:
                    print "%s\t%s\t%s\t%s\t%s\t%s" % ("NoMatch", _id.encode('utf-8'), url.encode('utf-8'), name.encode('utf-8'), ls_tel.encode('utf-8'), ls_addr.encode('utf-8'))
            

def convert_latlng():
    for r in session.execute("select * from restaurant_nm_coordinate where isbaiducoordinate='T'"):
        rid = r[4]
        lat = r[6].encode('utf-8')
        lng = r[7].encode('utf-8')
        ins = ptpq_session.query(NMLatLng).filter(NMLatLng.rid==int(rid)).first()
        if not ins:
            coords = convert_baidu_coords(lng, lat)
            if coords:
                glat = coords.get('lat', 0)
                glng = coords.get('lng', 0)
                if glat > 0:
                    item = NMLatLng(rid=int(rid), blat=lat, blng=lng, glat=glat, glng=glng)
                    ptpq_session.add(item)
                    print rid, lat, lng, glat, glng
    ptpq_session.commit()

if __name__ == '__main__':
    print get_city_url_to_gs()
    #rest_search()
    #convert_latlng()
