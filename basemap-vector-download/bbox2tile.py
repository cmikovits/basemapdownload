#!/usr/bin/python

import math
def deg2num(lon_deg, lat_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (ytile, xtile)

at1 = (9.47996951665, 46.4318173285)
at2 = (16.9796667823, 49.0390742051)

for z in range(1, 23):
    maxy, minx = deg2num(at1[0], at1[1], z)
    miny, maxx = deg2num(at2[0], at2[1], z)
    print("zoom: %d, y: %d-%d, x: %d-%d" % (z, miny, maxy, minx, maxx))
