#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import sys
import Levenshtein
import math
import requests
from pyes import *
from pyes.filters import *
from pyes.facets import *
from pyes.sort import *
sys.path.append("/home/chenyp/Utils")
import traceback
from common.logger import *

_log = get_logger("search_es")

#INDEX_NAME = 'rest_index'
#DOC_TYPE = "rest_type"
INDEX_NAME = 'poi_index'
DOC_TYPE = "poi_type"

conn = ES(("thrift", "127.0.0.1", "9500"))
#conn = ES('127.0.0.1:9200', timeout=3.5)#连接ES

def get_distance(lat1, lng1, lat2, lng2):
    """
    计算两个经纬度之间的距离(单位米)
    """
    rad = lambda d: d * math.pi / 180.0

    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
        math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_RADIUS
    return int(round(s * 1000.0))

def cosine_similarity(s1, s2):
    if not isinstance(s1, unicode):
        s1 = s1.decode('utf-8')
    if not isinstance(s2, unicode):
        s2 = s2.decode('utf-8')
    s1 = re.sub(u'\(|\)|（|）| ', u'', s1)
    s2 = re.sub(u'\(|\)|（|）| ', u'', s2)
    terms = list(set([i for i in s1+s2]))
    v1 = [0] * len(terms)
    v2 = [0] * len(terms)
    for i in xrange(len(terms)):
        if terms[i] in s1:
            v1[i] += 1
        if terms[i] in s2:
            v2[i] += 1
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for j in xrange(len(terms)):
        sum_xy += v1[j] * v2[j]
        sum_x2 += v1[j] ** 2
        sum_y2 += v2[j] ** 2
    return sum_xy / (math.sqrt(sum_x2) * math.sqrt(sum_y2))

def es_analyzer(analyzer="ik", text=""):
    ret = []
    payload = {"analyzer":analyzer, "pretty":"true"}
    if isinstance(text, unicode):
        text = text.encode('utf-8')
    r = requests.get("http://localhost:9200/poi_index/_analyze", params=payload, data=text)
    if r.status_code == 200:
        if 'tokens' in r.json():
            for c in r.json()['tokens']:
                ret.append(c['token'])
    return ret

def search_poi(keyword='', district_id=0, alias='', tel='', lat=0, lon=0, radius=5000, length=10, sort=""):
    _log.info("keyword: %s\tdistrict_id: %s" % (keyword, district_id))
    ret = []
    must_f = []
    bq = []
    bq1 = []
    bq2 = []
    if keyword:
        full_name_q = TermQuery(u"name2", keyword, boost=100)
        bq1.append(full_name_q)
        for w in es_analyzer(text=keyword, analyzer="ik_smart"):
            name_q = TermQuery(u"name", w, boost=0.1)
            bq1.append(name_q)
        #店铺名称以及分店名词分开进行搜索
        if not isinstance(keyword, unicode):
            keyword = keyword.decode('utf-8')
        keyword_segs = re.split(u'\(|\)|（|）| ', keyword)
        if len(keyword_segs) >= 2:
            for w in es_analyzer(text=keyword_segs[0], analyzer="ik_smart"):
                name3_q = TermQuery(u"brand_name", w, boost=0.4)
                bq1.append(name3_q)
            for w in es_analyzer(text=keyword_segs[1], analyzer="ik_smart"):
                name4_q = TermQuery(u"road_name", w, boost=0.2)
                bq1.append(name4_q)
            
    if alias:
        for w in es_analyzer(text=alias):
            alias_q = TermQuery(u"alias", w, boost=0.75)
            bq1.append(alias_q)
    if district_id > 0:
        district_q = TermQuery(u"district_path", str(district_id))
        bq2.append(district_q)
    if must_f:
        bf = BoolFilter(must=must_f)
        tq = FilteredQuery(BoolQuery(should=bq1), bf)
    else:
        tq = BoolQuery(should=bq1, must=bq2)
    #my_custom_query = FunctionScoreQuery(query=tq, functions=[FunctionScoreQuery.ScriptScoreFunction(script="_score + (20 - doc['str_length'].value) / 20.0")])
    #s = Search(my_custom_query)
    s = Search(tq)
    #print s.serialize()
    try:
        resultset = conn.search_raw(s, INDEX_NAME, DOC_TYPE, start=0, size=length, sort=sort)
        for row in resultset['hits']['hits']:
            r = row['_source']
            if 'location' in r:
                if 'lat' in r['location']:
                    r_lat, r_lon = float(r['location']['lat']), float(r['location']['lon'])
            else:
                r_lat, r_lon = (0, 0)
            
            row = { 'id'    : r['id'],
                    'name'  : r['name'],
                    'tel'  : r['tel'],
                    'address'  : r['address'],
                    'lat'   : r_lat,
                    'lon'   : r_lon,
                    'score' : row["_score"]
                    }
            if keyword and r['name']:
                r_name = r['name']
                if isinstance(keyword, unicode):
                    keyword = keyword.encode('utf-8')
                if isinstance(r_name, unicode):
                    r_name = r_name.encode('utf-8')
                keyword = re.sub('\(|\)|（|）| ', '', keyword)
                r_name = re.sub('\(|\)|（|）| ', '', r_name)
                row['Levenshtein_ratio'] = Levenshtein.ratio(keyword.lower(), r_name.lower())
                row['cosine_similarity'] = cosine_similarity(keyword.lower(), r_name.lower())
            if (lat != 0 or lon != 0) and (r_lat !=0 or r_lon !=0):
                row['distance'] = get_distance(lat, lon, r_lat, r_lon)
            ret.append(row)
        rs = {'cost':resultset.took, 'total': resultset['hits']['total'], 'data': ret}
        return rs
    except Exception,e:
        _log.error("keyword: %s\n%s" % (keyword, traceback.format_exc()))
    return {'data': ret, 'total': 0}
    

if __name__ == '__main__':
    for i in search_poi(keyword=u"农耕年华农业风情园", length=5)['data']:
        print i['id'], i['name'], i['Levenshtein_ratio'], i['cosine_similarity']

