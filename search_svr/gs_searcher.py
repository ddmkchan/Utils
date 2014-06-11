#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import Levenshtein
import math
import requests
from pyes import *
from pyes.filters import *
from pyes.facets import *
from pyes.sort import *

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
            #name_q = TermQuery(u"name", w, boost=0.1)
            #name_q = MatchQuery(u"name", keyword, analyzer="ik", operator="or", minimum_should_match="1%")
            bq1.append(name_q)
    if alias:
        for w in es_analyzer(text=alias):
            #alias_q = MatchQuery(u"alias", alias, analyzer="ik", operator="or", minimum_should_match=2)
            alias_q = TermQuery(u"alias", w, boost=0.75)
            bq1.append(alias_q)
    if district_id > 0:
        district_q = TermQuery(u"district_path", str(district_id))
        bq2.append(district_q)
        #must_f.append(TermFilter("district_id", district_id))
    #if lat != 0 and lon != 0:
    #    must_f.append(GeoDistanceFilter("location", {"lat" : lat, "lon" :lon}, "%fkm" % (radius/1000.0)))
    if must_f:
        bf = BoolFilter(must=must_f)
        tq = FilteredQuery(BoolQuery(should=bq1), bf)
    else:
        tq = BoolQuery(should=bq1, must=bq2)
    #print tq.serialize()
    s = Search(tq)
    #resultset = conn.search(tq, INDEX_NAME, DOC_TYPE, start=0, size=length)
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
            if not isinstance(keyword, unicode):
                keyword = keyword.decode('utf-8')
            if not isinstance(r_name, unicode):
                r_name = r_name.decode('utf-8')
            row['Levenshtein_ratio'] = Levenshtein.ratio(keyword, r_name)
            row['cosine_similarity'] = cosine_similarity(keyword, r_name)
        if (lat != 0 or lon != 0) and (r_lat !=0 or r_lon !=0):
            row['distance'] = get_distance(lat, lon, r_lat, r_lon)
        ret.append(row)
        #print r.id, r.name, r._meta["score"], r.location
    rs = {'cost':resultset.took, 'total': resultset['hits']['total'], 'data': ret}
    return rs

def facet_demo():
    q2 = MatchAllQuery().search()
    #print dir(q2.facet)
    #print dir(q2.facet.facets), type(q2.facet.facets)
    #q2.facet.facets.append(RangeFacet("range1", field="district_id", ranges = [
    #                { "to" : 500 },
    #                { "from" : 2000, "to" : 7000 },
    #                { "from" : 7000, "to" : 12000 },
    #                { "from" : 15000 }]))
    q2.facet.facets.append(TermFacet("district_id"))
    #q2.facet.add_term_facet("district_id", size=20)
    print q2
    resultset = conn.search(q2, INDEX_NAME, DOC_TYPE, size=10)
    print resultset.facets

def geo_distance_demo():
    must_f = []
    bq1 = []
    lon = 115.797986
    lat = 33.811545
    radius = 500000
    name_q = MatchQuery(u"name", u"图巴", analyzer="ik", operator="or", minimum_should_match=3)
    bq1.append(name_q)
    must_f.append(GeoDistanceFilter("location", {"lat" : lat, "lon" :lon}, "%fkm" % (radius/1000.0)))
    bf = BoolFilter(must=must_f)
    tq = FilteredQuery(BoolQuery(should=bq1), bf)
    _sort = {
            "_geo_distance" : {
                "location" : [lat, lon],
                "order" : "desc",
                "unit" : "km"
            }
        }
    s = Search(name_q, sort=[_sort])
    resultset = conn.search_raw(s, INDEX_NAME, DOC_TYPE, size=1)
    #print resultset
    #for i in resultset:
    #    print i
    print '-------------------'
    for ret in resultset['hits']['hits']:
        print ret
        print ret['_source']['name']
    

if __name__ == '__main__':
    #q = MatchQuery(u"name", u"长风海洋世界", analyzer="ik", operator="or", minimum_should_match=4)
    #q = QueryStringQuery("九乡", u"name")
    #print search_poi(keyword="棒棰岛")
    #for j in _analyzer(analyzer="standard", text=u"故宫"):
    #    print j
    #print _analyzer()
    #print search_poi(keyword=u"公园", alias=u"紫禁城,故宫博物院")
    #cosine_similarity(u"故", u"琴台故径")
    #print Levenshtein.ratio(u"故", u"琴台故径")
    #for i in search_poi(keyword=u"公园", alias=u"紫禁城,故宫博物院")['data']:
    #    print i
    #search_poi(keyword=u"园", lon=116.281097, lat=39.997852, radius=500000)
    #print sort
    #sort=[{'_geo_distance': {'unit': 'km',
    #                                'order': 'desc',
    #                                'location': '115.797986,33.811545'}}] 
    #print search_poi(keyword=u"长")
    #for i in search_poi(keyword=u"农耕年华农业风情园", length=5)['data']:
    #    print i['id'], i['name'], i['Levenshtein_ratio'], i['cosine_similarity']
    #print search_poi(keyword="王陵", alias="老君")
    #geo_distance_demo()
    print es_analyzer(text="阿拉善盟", analyzer="ik_smart")
    #print cosine_similarity("广州市荔湾区龙津西路庙前街（荔湾湖公园旁）。", "龙津西路逢源北街84号")
    #print get_distance(30.6081639999772, 114.424017000088, 30.717745,114.466965)
