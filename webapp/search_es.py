import tornado.ioloop
import tornado.web
import json
import sys
sys.path.append("/home/chenyp/Utils")
from search_svr import gs_searcher
from search_svr import gs_rest_searcher
from search_svr import gs_course_searcher

class SearchPoiHandler(tornado.web.RequestHandler):
    def get(self):
        _keyword = self.get_argument('keyword', '')
        _alias = self.get_argument('alias', '')
        _district_id = int(self.get_argument('district_id', 0))
        _lat = float(self.get_argument('lat', 0))
        _lon = float(self.get_argument('lon', 0))
        _radius = int(self.get_argument('radius', 5000))
        _length = int(self.get_argument('length', 10))
        _sort = self.get_argument('sort', '')
        self.write(json.dumps(gs_searcher.search_poi(keyword=_keyword, district_id=_district_id, alias=_alias, lat=_lat, lon=_lon, radius=_radius, length=_length, sort=_sort)))

class SearchRestHandler(tornado.web.RequestHandler):
    def get(self):
        _keyword = self.get_argument('keyword', '')
        _alias = self.get_argument('alias', '')
        _district_id = int(self.get_argument('district_id', 0))
        _lat = float(self.get_argument('lat', 0))
        _lon = float(self.get_argument('lon', 0))
        _radius = int(self.get_argument('radius', 5000))
        _length = int(self.get_argument('length', 10))
        _sort = self.get_argument('sort', '')
        self.write(json.dumps(gs_rest_searcher.search_poi(keyword=_keyword, district_id=_district_id, alias=_alias, lat=_lat, lon=_lon, radius=_radius, length=_length, sort=_sort)))

class SearchCourseHandler(tornado.web.RequestHandler):
    def get(self):
        _keyword = self.get_argument('keyword', '')
        _sort = self.get_argument('sort', '')
        _length = int(self.get_argument('length', 10))
        self.write(json.dumps(gs_course_searcher.search_poi(keyword=_keyword, length=_length, sort=_sort)))

