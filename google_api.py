#!usr/bin/env python
#-*- coding:utf-8 -*-

import requests
import json

_s = requests.session()

def g():
	URL = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCAOJ2hRiHF959HK6z60Y4BW8yImHwWQ4g"
	payload = {
 "homeMobileCountryCode": 460,
 "homeMobileNetworkCode": 0,
 "cellTowers": [
  {
   "cellId": 11013,
   "locationAreaCode": 10065,
   "mobileCountryCode": 460,
   "mobileNetworkCode": 0
  }
 ],
"wifiAccessPoints":[]
}
	#payload = open("d2.json").read()
	#print json.loads(payload)
	headers = {'Content-Type': 'application/json'}
	r = requests.post(URL, data=json.dumps(payload), timeout=10, headers=headers)
	print r.text

def func():
	payload = {"apis": '{"installment":{"data":{"car_id":"59424f2c762d959d"},"request_type":"get"},"detail":{"data":{"car_id":"59424f2c762d959d"},"request_type":"get"}}'}
	#r = requests.post("http://api.renrenche.com/system/relax?mobile=&im=868008021955269&mb=Che2-UL00&os=android&ov=4.4.2&sv=1.8.4&city=%E5%8C%97%E4%BA%AC&uuid=0742fa14-1fd3-4193-8b9c-1ac1c7a52303&channel=QQ_20151009", data=payload, headers=headers)
	r = requests.get("http://api.renrenche.com/system/relax", params=payload)
	print r.url
	print r.json()


if __name__ == '__main__':
	func()
