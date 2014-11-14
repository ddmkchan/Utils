#!/usr/bin/env python
#-*- coding:utf-8-*-

import os
import re
import sys
sys.path.append("/home/chenyp/Utils")
import traceback
from common.define import *
from pyes import *
from db import Dao

dao = Dao()

class poi_seatch(object):

    def __init__(self):
        self._index = "poi_index"
        self._type = "poi_type"
        self.conn = ES('127.0.0.1:9200', timeout=3.5)#连接ES
        #获取两个切换index名
        self._alias = ['poi_index_1', 'poi_index_2']
        try:
            self.current_alias = self.conn.indices.get_alias(self._index)
        except Exception,e:
            print e
            self.current_alias = None

        if self.current_alias:
            self.current_alias = self.current_alias[0]
        else:
            self.current_alias = None

        if self.current_alias == self._alias[0]:
            self.tmp_index = self._alias[1]
        else:
            self.tmp_index = self._alias[0]
        print self.current_alias,'->',self.tmp_index


    def init_index(self):
        #定义索引存储结构
        mapping = {u'id': {'store': 'yes',
                          'type': u'integer'
                            },
                  u'district_id': {'index': 'not_analyzed',
                             'store': 'yes',
                             'type': u'integer'
                             },
                  u'district_path': {'index': 'analyzed',
                             'store': 'yes',
                             'type': u'string',
                             "indexAnalyzer":"whitespace",
                             "searchAnalyzer":"whitespace",
                             "term_vector" : "with_positions_offsets"},
                  u'name': {'index': 'analyzed',
                             'store': 'yes',
                             'type': u'string',
                             "indexAnalyzer":"ik_smart",
                             "searchAnalyzer":"ik_smart",
                             "term_vector" : "with_positions_offsets"},
                  u'name2': {'index': 'not_analyzed',
                             'store': 'yes',
                             'type': u'string'},
                  u'tel': {'index': 'not_analyzed',
                             'store': 'no',
                             'type': u'string'},
                  u'alias': {'index': 'analyzed',
                             'store': 'yes',
                             'type': u'string',
                             "indexAnalyzer":"ik",
                             "searchAnalyzer":"ik",
                             "term_vector" : "with_positions_offsets"},
                  u'address': {'index': 'analyzed',
                             'store': 'yes',
                             'type': u'string',
                             "indexAnalyzer":"ik",
                             "searchAnalyzer":"ik",
                             "term_vector" : "with_positions_offsets"},
                  u"location": {"type": "geo_point",
                                "store": "yes",
                                "normalize": "yes",
                                "lat_lon": "yes"
                                },
                }
        self.conn.indices.delete_index_if_exists(self.tmp_index)
        self.conn.indices.create_index(self.tmp_index)#新建一个索引

        self.conn.indices.put_mapping(self._type, {'properties':mapping}, [self.tmp_index])

    def add_doc(self):
        #rs = get_data_from_file('gs_sight')
        rs = get_sight_data()
        for ret in rs:
            doc = {}
            doc["id"] = ret.get("id")
            doc["district_id"]  = ret.get("district_id")
            doc["district_path"]  = ret.get("district_path")
            doc["name"] = ret.get("name")
            doc["name2"] = ret.get("name2")
            doc["alias"] = ret.get("alias")
            doc["address"] = ret.get("address")
            doc["tel"] = ret.get("tel")
            if ret.get("coords")["lon"] != 0 and ret.get("coords")["lat"] != 0:
                doc["location"]  = {"lon": round(ret.get("coords")["lon"], 6), 
                            "lat": round(ret.get("coords")["lat"], 6)}
            self.conn.index(doc, self.tmp_index, self._type)

    def rebuild_all(self):
        self.conn.force_bulk()
        self.conn.bulk_size = 10000
        self.conn.raise_on_bulk_item_failure = False
        
        self.add_doc()
        self.conn.indices.refresh()

    def switch_alias(self):
        if self.current_alias == self._index:
            self.conn.indices.delete_index_if_exists(self._index)
            self._switch_alias(None, self.tmp_index)
        else:
            self._switch_alias(self.current_alias, self.tmp_index)

    def _switch_alias(self, from_index_name, to_index_name):
        actions = []
        if from_index_name:
            actions.append(('remove', from_index_name, self._index, {}))
        actions.append(('add', to_index_name, self._index, {}))
        print "actions ", actions
        self.conn.indices.change_aliases(actions)

def get_data_from_file(filename):
    rs = []
    _path = "%s/%s" % (os.getcwd(), filename)
    f = open(_path)
    for i in f.readlines()[:]:
        segs = i.rstrip().split("\t")
        rs.append({"id": int(segs[0]),
                    "district_id": int(segs[1]),
                    "name": segs[2],
                    "name2": segs[2],
                    "alias": segs[3],
                    "coords": {"lon":float(segs[4]), "lat":float(segs[5])},
                    })
    f.close()
    return rs

def get_sight_data():
    #s = get_sale_sight()
    rs = []
    ret = dao.conn().execute("select s.SightId, s.DistrictId, s.Name, s.Alias, s.Lon, s.Lat, s.Address, Tel, isnull(d.districtpath, '') from dbo.sight s left join dbo.districtinfo d on s.DistrictId = d.DistrictId where s.publishstatus=6")
    for r in ret:
        p_district_ids = re.split('\.', r[8])
        rs.append({'id': int(r[0]),
                    'district_id': int(r[1]),
                    "district_path": " ".join([i for i in p_district_ids if len(i) > 0]),
                    'name': r[2],
                    'name2': r[2],
                    "alias": r[3],
                    "coords": {"lon":float(r[4]), "lat":float(r[5])},
                    "address": r[6],
                    "tel": r[7],
                    })
    return rs

def get_sale_sight():
    #在线销售POI
    import xlrd
    wb = xlrd.open_workbook("dp-0527.xlsx")
    sh = wb.sheets()[0]
    return [int(sh.row_values(i)[0]) for i in xrange(1, sh.nrows)]
    #print sh.row_values(i)[0]

if __name__ == '__main__':
    #print len(get_sight_data())
    poi = poi_seatch()
    poi.init_index()
    poi.rebuild_all()
    poi.switch_alias()
    #get_data_from_file('gs_sight')
    #get_sale_sight()
