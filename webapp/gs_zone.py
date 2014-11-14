import tornado.ioloop
import tornado.web
import json
import sys
sys.path.append("/home/chenyp/Utils")
from poly.restaurant_zone import *

def get_zone_range_by_zone_id(zone_id):
    #return [{"lng": float(row[1]), "lat": float(row[2])}for row in poidb.conn().execute("select Zone, PointLon, PointLat from dbo.ZoneRange where PointType=1 and zone=%s" % zone_id)]
    lats = []
    lngs = []
    for row in poidb.conn().execute("select Zone, PointLon, PointLat from dbo.ZoneRange where PointType=1 and zone=%s" % zone_id):
        lats.append(float(row[2]))
        lngs.append(float(row[1]))
    points = numpy.array([lats, lngs])
    pts = convex_hull([(p[1], p[0]) for p in points.transpose()])
    return [{"lng": row[0], "lat": row[1]}for row in pts]

def get_rest_by_rest_id(rest_id):
    mydict = {}
    try:
        for row in destdb.conn().execute("select Lon, Lat from dbo.Restaurant where RestaurantId=%s" % rest_id):
            mydict['lng'] = float(row[0])
            mydict['lat'] = float(row[1])
    except Exception,e:
        pass
    return mydict 


class GetZoneRangeHandler(tornado.web.RequestHandler):
    def get(self):
        zid = self.get_argument('zid', 0)
        self.write(json.dumps(get_zone_range_by_zone_id(zid)))


class GetRestaurantHandler(tornado.web.RequestHandler):
    def get(self):
        rid = self.get_argument('rid', 0)
        self.write(json.dumps(get_rest_by_rest_id(rid)))


if __name__ == "__main__":
    print get_zone_range_by_zone_id(4209)
