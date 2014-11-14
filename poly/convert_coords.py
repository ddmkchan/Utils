#!/usr/bin/python
#coding=utf-8

import requests
import traceback

def convert_mapbar_coords(lng, lat):

    '''
    Return product detail by source name and product id
    '''
    payload = {
        'sid': '15001',
        'src': 'mapbar',
        'resType': 'json',
        'Key': '0026ff5ef64722f9099cc4d7b1f1be33',
        'xys': '%s,%s' % (lng, lat)
    }
    try:
        r = requests.get(url='http://restapi.amap.com/coordinate/simple', params=payload, timeout=5.1)
        print r.url
        resp = r.json() if r else None
        if resp and resp['status'] == 'E0':
            return {'lng':resp['xys'].split(',')[0], 'lat':resp['xys'].split(',')[1]}
        else:
            print '@@@@@'
            return None
    except:
        print 'eeee'
        print traceback.format_exc()
        return None


def convert_gaode_coords(lng, lat):

    '''
    Return product detail by source name and product id
    '''
    payload = {
        'sid': '15001',
        'src': 'mapbar',
        'resType': 'json',
        'Key': '0026ff5ef64722f9099cc4d7b1f1be33',
        'xys': '%s,%s' % (lng, lat)
    }
    try:
        r = requests.get(url='http://restapi.amap.com/coordinate/simple', params=payload, timeout=5.1)
        print r.url
        print r.text, "-------------"
        resp = r.json() if r else None
        if resp and resp['status'] == 'E0':
            return {'lng':resp['xys'].split(',')[0], 'lat':resp['xys'].split(',')[1]}
        else:
            print '@@@@@'
            return None
    except:
        print 'eeee'
        print traceback.format_exc()
        return None


if __name__ == '__main__':
    coords = convert_gaode_coords('116.06509464165269', '39.63607428168995')
    print coords
