import csv
import numpy as np
import matplotlib.pyplot as plt
import math as m
import pymap3d as pm
from datetime import datetime
import time
import sys


#----Checking whether the Balloon was close to----
#                  ARA5 or not

def BalloonThreshold(filepath):
    latitudes = []
    longitudes = []
    altitudes = []
    times = []
    with open(filepath) as tsvfile:
        tsvreader = csv.reader(tsvfile)
        for x in range(0,3):
            next(tsvreader)
        for row in tsvreader:
            datetime1 = datetime.strptime(row[0].strip(),"%Y-%m-%dT%H:%M:%S")
            timestamp1 = time.mktime(datetime1.timetuple())
            #print(timestamp1)
            break

    with open(filepath) as tsvfile:
        tsvreader = csv.reader(tsvfile)
        for x in range(0,8):
            next(tsvreader)
        for row in tsvfile:
            line = row.split()
            if len(line) != 0:
                longitudes.append(float(line[13]))
                latitudes.append(float(line[14]))
                altitudes.append(float(line[5]))
                times.append(float(line[0]))
                #print(longitudes)
                #print(latitudes)
                #print(altitudes)
                #print(times)

    #----Converting times into unix times----
    unixtimes = []
    for t in range(0,len(times)):
        T = t + timestamp1
        unixtimes.append(T)

    #print(unixtimes)

    #Coordinates of ARA5
    a5_lon = -121.03
    a5_lat = -89.93
    a5_alt = -170.0


    #----Finding the distance between the balloon and ARA5----
    def FindenuCoordinates(lat,lon,alt):
        point_e = np.zeros(len(lat))
        point_n = np.zeros(len(lat))
        point_u = np.zeros(len(lat))
        for x in range(0,len(lat)):
            (point_e[x],point_n[x],point_u[x]) = pm.geodetic2enu(lat[x],lon[x],alt[x],a5_lat,a5_lon,a5_alt)
        return point_e, point_n, point_u

    a5_e,a5_n,a5_u = (0,0,0) 

    def distance(x1,y1,z1,x2,y2,z2):
        d = m.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        return d

    def FindDistances(lat,lon,alt):
        ball_e, ball_n, ball_u = FindenuCoordinates(lat,lon,alt)
        d_a5 = np.zeros(len(lat))
        for z in range(0,len(ball_e)):
            d_a5[z] = distance(a5_e, a5_n, a5_u, ball_e[z], ball_n[z], ball_u[z])
        return d_a5

    d_ara5 = FindDistances(latitudes,longitudes,altitudes)
    #print(d_ara5)


    #----Plots relevant to ARA5----
    plt.figure(1)
    plt.scatter(longitudes,latitudes)
    plt.title("Latitude vs. Longitude")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    plt.figure(2)
    plt.scatter(times,altitudes)
    plt.title("Altitude vs. Time")
    plt.xlabel("Time")
    plt.ylabel("Altitude")

    plt.figure(3)
    plt.title("Histogram of distances of Balloon from ARA5")
    plt.xlabel("Distances")
    plt.hist(d_ara5)

    plt.figure(4)
    plt.title("Distance of Balloon from ARA5 over time")
    plt.xlabel("Time")
    plt.ylabel("Distance")
    plt.scatter(times,d_ara5)
    #plt.show()

     #----Testing Threshold----
    threshold = 20000

    thresholdtimes = []
    for x in range(0,len(d_ara5)):
        if m.floor(d_ara5[x]) > threshold:
            dmax = x
            break

    print(dmax)
    for x in range(0,dmax):
        thresholdtimes.append(unixtimes[x])

    return thresholdtimes
