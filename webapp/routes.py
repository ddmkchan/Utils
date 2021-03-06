import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")

class MainHandler2(tornado.web.RequestHandler):

    def get(self):
        lat = self.get_argument('lat', 0)
        lng = self.get_argument('lng', 0)
        self.render("index.html", lat=lat, lng=lng)

class AjaxHandler(tornado.web.RequestHandler):

    def get(self):
        tmp = {'name': 'ddmk'}
        self.write(json.dumps(tmp))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/shangquan", MainHandler2),
    (r"/forjs", AjaxHandler),
    #(r"/globalpoi", g_poi.GetGlobalPOIHandler),
    #(r"/tc_scenery_detail", tc.GetSceneryDetailBySidHandler),
    #(r"/tc_scenery_list", tc.GetSceneryListHandler),
    #(r"/tc_image_list", tc.GetSceneryImageListHandler),
    #(r"/poi_search", search_es.SearchPoiHandler),
    #(r"/rest_search", search_es.SearchRestHandler),
    #(r"/course_search", search_es.SearchCourseHandler),
    #(r"/gs_zone", gs_zone.GetZoneRangeHandler),
    #(r"/restaurant", gs_zone.GetRestaurantHandler),
])

