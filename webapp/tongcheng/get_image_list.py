#!/urs/bin/python
#coding=utf-8

import re
import json
from datetime import datetime
from lxml import etree
from tc_common import *
import xmltodict
from time import *
from XMLtoJSON import XMLtoJSON
import sys
sys.path.append("/home/chenyp/myscrapy/guba")
from define import *


clientIp = "211.136.149.94"
servicename = "GetSceneryImageList"
pagesize = 100

_xml = """
<request>
    <header>
        <version>%s</version> 
        <accountID>%s</accountID>
        <serviceName>%s</serviceName> 
        <digitalSign>%s</digitalSign> 
        <reqTime>%s</reqTime>
    </header>
    <body>
        <sceneryId>%s</sceneryId>
        <page>%d</page>
        <pageSize>%d</pageSize>
    </body>
</request>
"""

def escape_chr(line):
    line = re.sub('\\\\|\r|\n', '', line)
    return ''.join(c for c in line if ord(c) >= 32)


def get_scenery_detail_by_sid(sid):
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename="GetSceneryDetail", reqtime=_reqtime)
        req_xml = _xml2%(version, accountid, "GetSceneryDetail", digitalSign, _reqtime, sid)
        result = get_reponse(req_xml=req_xml)
        root = etree.XML(result)
        scenery_detail = root.find('body').find('scenery')
        lon = scenery_detail.find('lon').text
        lat = scenery_detail.find('lat').text
        return "%s,%s" % (lon, lat)
        #convertedDict = XMLtoJSON(input_string=escape_chr(result)).parse();
        #mydict = json.loads(convertedDict)
        #print mydict.get("lon")
        #print mydict.get("lat")
        #print "************", type(convertedDict), type(mydict)
        #return mydict["response"]
        #return convertedDict
    except Exception,e:
        print traceback.format_exc()
    return None
    
def get_image_list_by_sid(sid):
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename=servicename, reqtime=_reqtime)
        req_xml = _xml%(version, accountid, servicename, digitalSign, _reqtime, sid, 1, 10)
        #print req_xml
        result = get_reponse(req_xml=req_xml)
        convertedDict = xmltodict.parse(result);
        #print "************", convertedDict
        return convertedDict
    except Exception,e:
        print traceback.format_exc()
    return None

if __name__ == '__main__':
    get_image_list_by_sid(10487)
