#!/usr/bin/env python3
import sys
import os
import requests
import time
import random
import gdal
import ogr
import math

def deg2num(lon_deg, lat_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (ytile, xtile)

def num2deg(xtile, ytile, zoom):
  n = 2.0 ** zoom
  lon_deg = xtile / n * 360.0 - 180.0
  lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
  lat_deg = math.degrees(lat_rad)
  return (lat_deg, lon_deg)

server = "http://tile.poloha.net/budovy/" # 7/67/44.pbf
zoomLevel = 15

# 'CH': ('Switzerland', (6.02260949059, 45.7769477403, 10.4427014502, 47.8308275417)),

country = (15.2401111182, 48.5553052842, 16.8531441586, 59.1172677679)

maxY, minX = deg2num(country[0], country[1], zoomLevel)
minY, maxX = deg2num(country[2], country[3], zoomLevel)

# minX = 8624 #17251
# maxX = 8972 #17945
# minY = 5624 #11250
# maxY = 5804 #11608

numberOfRequests = 0
pauseAfterRequests = 1000
pauseInSeconds = 1

totalNumberOfTiles = (maxX - minX + 1) * (maxY - minY + 1)
numberOfTilesProcessed = 0

print("That's %d tiles total." % (totalNumberOfTiles))

# Loop through all tiles
for x in range(minX, maxX + 1):
    for y in range(minY, maxY + 1):
        directory = "basemap/%d/%d/" % (zoomLevel, x)
        file = directory + "%d.png" % (y)

        if not os.path.isfile(file):
            numberOfRequests += 1

            query = "%d/%d/%d.png" % (zoomLevel, x, y)

            # Issue the GET request
            randomServer = server # % (random.randint(1, 4))
            print("Issuing request " + randomServer + query + "...")
            try:
                r = requests.get(randomServer + query)
            except requests.exceptions.ConnectionError:
                print("ConnectionError thrown. Waiting one minute...")
                # Wait a minute
                time.sleep(60)
                r = requests.get(randomServer + query)

            # Create the directories if they don't exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            if r.status_code == requests.codes.ok:
                print("%d %d was found. Saving file." % (x, y))

                with open(file, 'wb') as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            elif r.status_code == requests.codes.not_found:
                print("%d %d could not be found (HTTP 404)." % (x, y))
            else:
                print("HTTP error %d occurred while downloading %d %d." % (r.status_code, x, y))

            if numberOfRequests >= pauseAfterRequests:
                time.sleep(pauseInSeconds)
                numberOfRequests = 0
        else:
            print("Tile %d %d already exists." % (x, y))

        numberOfTilesProcessed += 1
        percent = numberOfTilesProcessed / totalNumberOfTiles * 100
        print(" --- Processed %d / %d (%.3f percent)" % (numberOfTilesProcessed, totalNumberOfTiles, percent))
        
 
