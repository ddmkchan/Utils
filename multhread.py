#!/usr/bin/python
#coding=utf-8

import requests
import Queue
import threading
import socket
socket.setdefaulttimeout(30)#

q = Queue.Queue(0)
NUM_WORKERS = 5

class MyThread(threading.Thread):
    #继承父类threading.Thread，并修改run方法
    def __init__(self, input, func):
        threading.Thread.__init__(self)
        self._jobq = input
        self.func = func

    def run(self):
        while True:
            if self._jobq.qsize()>0:
                job = self._jobq.get()
                self.func()
            else:
                break
def func():
    url = "http://192.168.82.8:8040/tip/search"
    payload = {
            "keyword": "蛋糕",
            "type": 6,
            "districtid" : "",
            "needTokens" : False,
            "return" : "id,name,ename,district_id,district_name,in_china,tip_type",
            "sort" : "score:desc,popularity:desc",
            "section" : "0,20"
        }
    r = requests.post(url, params=payload)

def get_zone():
    #r = requests.get("http://10.2.8.172:8080/geometry/get_zone_range?lnglat=116.416784018278,39.9372464893734")
    #r = requests.get("http://172.16.125.1:8080/geometry/get_zone_range?lnglat=116.416784018278,39.9372464893734")
    #r = requests.get("http://10.8.74.16:8080/geometry/get_zone_range?lnglat=108.87986309839,34.2264619912354")
    r = requests.get("http://10.8.74.16:8080/geometry/get_zone_range?lnglat=102.72056702465,25.0206639155639")
    print len(r.json())

if __name__ == "__main__":
    #func()
    threads_arr = []
    for i in xrange(100):
        q.put(i)
    for x in range(NUM_WORKERS):
        t = MyThread(q, get_zone)
        threads_arr.append(t)
    for t in threads_arr:
        t.start()
    for t in threads_arr:
        t.join(timeout=1)

