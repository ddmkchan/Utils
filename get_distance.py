#!/usr/bin/python
#coding=utf-8

import math

def get_distance(lat1, lng1, lat2, lng2):
    """
    计算两个经纬度之间的距离(单位米)
    """
    lat1 = float(lat1)
    lng1 = float(lng1)
    lat2 = float(lat2)
    lng2 = float(lng2)
    rad = lambda d: d * math.pi / 180.0

    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    print radLat1, radLat2
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
        math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    s = s * EARTH_RADIUS
    return int(round(s * 1000.0))

if __name__ == "__main__":
    print get_distance(31.228307723999023, 121.49058532714844, 30.0704, 120.482)
    #print get_distance(31.2399, 121.5, 31.2320995330811, 121.472999572754)
    #print get_distance(39.97263, 116.3903, 39.89081, 116.39466)
    #print "hello"
