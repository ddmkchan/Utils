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
servicename = "GetSceneryList"
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
        <clientIp>%s</clientIp> 
        <cityId>%d</cityId>     
        <page>%d</page>
        <pageSize>%d</pageSize>
    </body>
</request>
"""

_xml2 = """
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
    </body>
</request>
"""

def addscenery(root):
    try:
        prefix = root.find(".//body//sceneryList").get("imgbaseURL")
    except AttributeError,e:
        prefix = ''
    try:
        scenerylist = root.find(".//body").getchildren()[0].getchildren()
    except (AttributeError,IndexError),e:
        pass
    else:
        for item in scenerylist:
            try:
                sceneryName = item.find(".//sceneryName").text
            except AttributeError, e:
                sceneryName = ''
            try:
                sceneryId = int(item.find(".//sceneryId").text)
            except AttributeError, e:
                sceneryId = 0
            try:
                sceneryAddress = item.find(".//sceneryAddress").text
            except AttributeError, e:
                sceneryAddress = ''
            try:
                scenerySummary = item.find(".//scenerySummary").text
            except AttributeError, e:
                scenerySummary = ''
            try:
                imgPath = item.find(".//imgPath").text
            except AttributeError, e:
                imgPath = ''
            try:
                provinceId = int(item.find(".//provinceId").text)
            except AttributeError, e:
                provinceId = 0
            try:
                provinceName = item.find(".//provinceName").text
            except AttributeError, e:
                provinceName = ''
            try:
                cityId = int(item.find(".//cityId").text)
            except AttributeError, e:
                cityId = 0
            try:
                cityName=item.find(".//cityName").text
            except AttributeError,e:
                cityName=''
            try:
                commentCount=int(item.find(".//commentCount").text)
            except AttributeError,e:
                commentCount=0
            try:
                questionCount=int(item.find(".//questionCount").text)
            except AttributeError,e:
                questionCount=0
            try:
                blogCount=int(item.find(".//blogCount").text)
            except AttributeError,e:
                blogCount=0
            try:
                viewCount=int(item.find(".//viewCount").text)
            except AttributeError,e:
                viewCount=0
            try:
                bookFlag=item.find(".//bookFlag").text
            except AttributeError,e:
                bookFlag=''
            try:
                sceneryAmount=item.find(".//sceneryAmount").text
            except AttributeError,e:
                sceneryAmount=0.0
            try:
                adviceAmount=item.find(".//adviceAmount").text
            except AttributeError,e:
                adviceAmount=0.0
            try:
                gradeId=item.find(".//gradeId").text
            except AttributeError,e:
                gradeId=''
            try:
                amount=item.find(".//amount").text
            except AttributeError,e:
                amount=0.0
            try:
                amountAdv=item.find(".//amountAdv").text
            except AttributeError,e:
                amountAdv=0.0
            try:
                distance=item.find(".//distance").text
            except AttributeError,e:
                distance=0
            themelist=''
            suitherdlist=''
            impressionlist=''
            try:
                themeList=item.find(".//themeList")
                ll=[]
                for i in themeList.getchildren():
                    ll.append(i.find(".//themeId").text)
                    #themelist='|'.join(i.find(".//themeId").text)
                themelist='|'.join(ll)
            except AttributeError,e:
                pass
            try:
                suitherdList=item.find(".//suitherdList")
                ll=[]
                for j in suitherdList.getchildren():
                    ll.append(j.find(".//suitherdId").text)
                    #suitherdlist='|'.join(j.find(".//suitherdId").text)
                suitherdlist='|'.join(ll)
            except AttributeError,e:
                pass
            try:
                impressionList=item.find(".//impressionList")
                ll=[]
                for k in impressionList.getchildren():
                    ll.append(k.find(".//impressionId").text)
                    #impressionlist='|'.join(k.find(".//impressionId").text)
                impressionlist='|'.join(ll)
            except AttributeError,e:
                pass
            current_time=datetime.now()
            obj=Session.query(TCScenery).filter(TCScenery.scenery_id==sceneryId).first()
            if obj:
                obj.comment_count=commentCount
                obj.question_count=questionCount
                obj.blog_count=blogCount
                obj.view_count=viewCount
                obj.theme_list=themelist
                obj.suitherd_list=suitherdlist
                obj.impression_list=impressionlist
                obj.scenery_amount=sceneryAmount
                obj.advice_amount=adviceAmount
                obj.amount=amount
                obj.amount_adv=amountAdv
                obj.book_flag=bookFlag
                obj.last_update=current_time
                obj.enabled=1
                Session.add(obj)
                Session.commit()
            else:
                item=TCScenery(scenery_id=sceneryId,scenery_name=sceneryName,scenery_address=sceneryAddress,scenery_summary=scenerySummary,img_path=prefix+imgPath,province_id=provinceId,province_name=provinceName,city_id=cityId,city_name=cityName,comment_count=commentCount,question_count=questionCount,blog_count=blogCount,view_count=viewCount,scenery_amount=sceneryAmount,advice_amount=adviceAmount,amount=amount,amount_adv=amountAdv,grade_id=gradeId,theme_list=themelist,suitherd_list=suitherdlist,impression_list=impressionlist,book_flag=bookFlag,last_update=current_time,create_date=current_time,enabled=1)
                Session.add(item)
                Session.commit()
        #sleep(5)

def gettotal():
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename=servicename, reqtime=_reqtime)
        req_xml = _xml%(version, accountid, servicename, digitalSign, _reqtime, clientIp, 0, 1, 1)
        result = get_reponse(req_xml=req_xml)
        root = etree.XML(result)
        scenerylist = root.find(".//body//sceneryList")
        return scenerylist.get("totalCount")
    except Exception,e:
        tc_log.error("gettotal\t%s"%traceback.format_exc())
    return 0

def main():
    _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    digitalSign = get_sign(servicename=servicename, reqtime=_reqtime)
    total = int(gettotal())
    if total > 0:
        if total % pagesize==0:
            page = total/pagesize
        else:
            page = total/pagesize+1
        for i in range(1, page+1):
            try:
                req_xml = _xml%(version, accountid, servicename, digitalSign, _reqtime, clientIp, 0, i, pagesize)
                result = get_reponse(req_xml=req_xml)
                if result:
                    tc_log.info("%s\t%s"%(i, page))
                    root = etree.XML(result)
                    addscenery(root)
            except Exception, e:
                tc_log.error("page:%s\t%s"%(i, traceback.format_exc()))

def add_ktb_city_id():
    f = open("%s/tongchengcity.txt"%DIR)
    for l in f.readlines():
        segs = l.rstrip().split('|')
        if segs[2]!='0':
            Session.execute("update tc_scenery set ktb_city_id=%d where city_id=%d"%(int(segs[2]), int(segs[1])))
    Session.commit()

def escape_chr(line):
    line = re.sub('\\\\|\r|\n', '', line)
    return ''.join(c for c in line if ord(c) >= 32)


def get_scenery_detail_by_sid(sid):
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename="GetSceneryDetail", reqtime=_reqtime)
        req_xml = _xml2%(version, accountid, "GetSceneryDetail", digitalSign, _reqtime, sid)
        result = get_reponse(req_xml=req_xml)
        print result
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
        print "%s\n%s" % (sid,traceback.format_exc())
    return None
    
def get_total():
    try:
        _reqtime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        digitalSign = get_sign(servicename=servicename, reqtime=_reqtime)
        req_xml = _xml%(version, accountid, servicename, digitalSign, _reqtime, clientIp, 0, 1, 1)
        print req_xml
        result = get_reponse(req_xml=req_xml)
        convertedDict = xmltodict.parse(result);
        print "************", type(convertedDict)
        return convertedDict
    except Exception,e:
        print traceback.format_exc()
    return None

if __name__ == '__main__':
    get_scenery_detail_by_sid(27273)
