#!/usr/bin/python
#coding=utf-8

class LatLng(object):
        
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class Bounds(object):
    
    def __init__(self, min_latlng, max_latlng):
        self.min_latlng = min_latlng
        self.max_latlng = max_latlng

    def contains(self, latlng):
        if latlng.lat < self.min_latlng.lat or\
            latlng.lat > self.max_latlng.lat or\
            latlng.lng < self.min_latlng.lng or\
            latlng.lng > self.max_latlng.lng:
            return False
        return True

class Polygon(object):

    def __init__(self, path):
        min_latlng = LatLng(min([latlng.lat for latlng in path]),
            min([latlng.lng for latlng in path]))
        max_latlng = LatLng(max([latlng.lat for latlng in path]),
            max([latlng.lng for latlng in path]))
        self.bounds = Bounds(min_latlng, max_latlng)
        self.path = path

    def containsLatLng(self, latlng):
        if self.bounds != None and not self.bounds.contains(latlng):
            return False

        inPoly = False
        j = len(self.path)-1
        for i in xrange(len(self.path)):
            vertex1 = self.path[i]
            vertex2 = self.path[j]

            if vertex1.lng < latlng.lng\
                and vertex2.lng >= latlng.lng\
                or vertex2.lng < latlng.lng\
                and vertex1.lng >= latlng.lng:
                if vertex1.lat + (latlng.lng - vertex1.lng) / (vertex2.lng - vertex1.lng) * (vertex2.lat - vertex1.lat) < latlng.lat:
                    inPoly = not inPoly
            j = i
        return inPoly

if __name__=="__main__":
    pass
