#!/usr/bin/python
#coding=utf-8

import os
import sys
import random,string
from time import sleep
import httplib
import urllib2
from datetime import datetime
import traceback
import socket

DIR = os.path.dirname(__file__)
LOG_DIR = "%s/log/"%DIR

version="20111128102912"
accountid="efa48793-c384-4857-a9c7-f11b3d1f7547"
accountkey="7b99af8e8552fe68"
#reqtime=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
socket.setdefaulttimeout(10)

def get_md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def get_sign(servicename='', reqtime=''):
    orginalarray=["Version="+version,"AccountID="+accountid,"ServiceName="+servicename, "ReqTime="+reqtime]
    sortedarrary=sorted(orginalarray)
    result = '&'.join(sortedarrary)
    result+=accountkey
    return get_md5(result)

def get_reponse(api_url="http://tcopenapi.17usoft.com/handlers/scenery/queryhandler.ashx", req_xml=''):
    request = urllib2.Request(
        url     = api_url,
        headers = {'Content-Type' : 'application/xml','charset':'UTF-8'},
        data    = req_xml)
    result = urllib2.urlopen(request)
    return result.read()
