import tornado.ioloop
import tornado.web
import json
import requests

def PoiService():
    url = "http://ws.you.ctripcorp.com/globalpoiservice/api/GetPoiList"
    headers = {
                'content-type': 'application/json',
                'accept': 'application/json'
                }
    payload = {
                "count": 100,
                "lastUpdateDate": "/Date(1401095406297-0000)/",
                "poiType": "ALL",
                "start": 1
                }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    return r.json()


class GetGlobalPOIHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(PoiService())
        #self.write(json.dumps(PoiService()))


if __name__ == "__main__":
    PoiService()
