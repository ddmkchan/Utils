#!/usr/bin/python
#coding=utf-8

import urllib
import os
from user_stat import *
import requests
import Queue
import threading
import traceback
import time
from logger import get_logger
import functools
import socket

logger = get_logger("ktb_images")

q = Queue.Queue(0)
NUM_WORKERS = 5

socket.setdefaulttimeout(30)#全局的socket超时, urlretrieve下载如果遇到网络异常，urlretrieve函数会一直在那下载，实际上什么也没下载下来，导致整个程序锁死

class MyThread(threading.Thread):
    #继承父类threading.Thread，并修改run方法
    def __init__(self, p, func):
        threading.Thread.__init__(self)
        self._jobq = p
        self.func = func

    def run(self):
        while True:
            if self._jobq.qsize()>0:
                params = self._jobq.get()
                self.func(params[0], params[1])
            else:
                break

def download_image(pic_name, path):
    try:
        if not os.path.isfile("%s/%s" % (path.rstrip(), pic_name)):
            #logger.info("del %s/%s " % (path, pic_name))
            #os.remove("%s/%s" % (path.rstrip(), pic_name))
            logger.info("downloading image... %s/%s" % (path, pic_name))
            _url = u"http://img.kantuban.com/pin/%s" % pic_name
            filename = "%s/%s" % (path.rstrip(), pic_name)
            urllib.urlretrieve(_url, filename)
        else:
            pass
            #logger.info("%s/%s exists" % (path, pic_name))
    except Exception,e:
        logger.error("%s\t%s\t%s\n%s" % ("Exception", path, pic_name, traceback.format_exc()))

def main():
    threads_arr = []
    bmap = get_board_map()
    sh = wb.sheets()[0]
    #for i in xrange(1, 3):
    for i in xrange(3, sh.nrows):
        if int(sh.row_values(i)[2]) >= 10:
            uid = sh.row_values(i)[0]
            uname = sh.row_values(i)[1]
            if uid not in [39, 157, 2150, 2452]:
                for p in session.execute("select pic_name, bid from tb_pin where deleted=0 and type='ADD' and source_url='' and uid = %s" % int(uid)):
                    bname = bmap.get(p[1], "")
                    if bname:
                        path = u"%s/%s/%s" % (DES_DIR, uname, bname)
                        q.put([p[0], path])
    for x in range(NUM_WORKERS):
        t = MyThread(q, download_image)
        t.setName("Thread_%s" % x)
        threads_arr.append(t)
    for t in threads_arr:
        t.start()
    for t in threads_arr:
        t.join()

if __name__ == "__main__":
    #func()
    main()
