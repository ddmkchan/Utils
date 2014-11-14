import tornado.ioloop
import tornado.web
import json
from tongcheng import tc_demo, get_image_list

class GetSceneryDetailBySidHandler(tornado.web.RequestHandler):
    def get(self):
        pid = self.get_argument('pid', 0)
        self.write(json.dumps(tc_demo.get_scenery_detail_by_sid(int(pid))))

class GetSceneryListHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(tc_demo.get_total()))

class GetSceneryImageListHandler(tornado.web.RequestHandler):
    def get(self):
        pid = self.get_argument('pid', 0)
        self.write(json.dumps(get_image_list.get_image_list_by_sid(pid)))

class GetSceneryImageListV2Handler(tornado.web.RequestHandler):
    def get(self):
        pid = self.get_argument('pid', 0)
        self.write(json.dumps(get_image_list.get_image_list_by_sid(pid)))
