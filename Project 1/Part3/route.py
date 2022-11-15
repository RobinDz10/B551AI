#!/usr/local/bin/python3
# route.py : Find routes through maps
#
#
# Based on skeleton code by V. Mathur and D. Crandall, Fall 2022
#


# !/usr/bin/env python3
import sys
import queue
import numpy as np

# a dictionary that can accept duplicate keys, append new element in list
class DictDuplicateKeys(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(DictDuplicateKeys, self).__setitem__(key, [])
        self[key].append(value)

def heuristic(currLatLon, endLatLon):
    # approximate radius of earth in mile
    R = 3958.8
    lat1, lon1 = np.radians(currLatLon)
    lat2, lon2 = np.radians(endLatLon)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    currLatLon = np.radians(currLatLon)
    endLatLon = np.radians(endLatLon)

    #Haversine formula - compute distance between two Lat/Lon
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c

#generate approximate Lat/Lon
def heuristic2(endLatLon, direction, length, currentName, parentLatLon, gpsDict):
    
    latLength = length * direction[1]
    longLength = length * direction[0]

    #Approximate, not accurate distance
    # 1 dgree of latitude = 69.04117454 miles
    currentLat = parentLatLon[0] + latLength / 69.04117454
    # 1 dgree of longitude = 69.04117454 miles * cos( parent's Latitude )
    currentLon = parentLatLon[1] + longLength / (69.04117454 * np.cos(np.radians(parentLatLon[0])))
    
    currentLatLon = np.array([currentLat, currentLon])
    gpsDict[currentName] = currentLatLon
    return heuristic(currentLatLon, endLatLon)

#bearing - direction vector(North, East) between two Lat/Lon 
def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = np.cos(np.radians(lat2)) * np.sin(np.radians(dLon))
    y = np.cos(np.radians(lat1)) * np.sin(np.radians(lat2)) - np.sin(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.cos(np.radians(dLon))
    return np.array([x, y]) / np.linalg.norm([x, y])

#get path from closedList
                    #[0]city name, [1]parent, [2]G(n), [3]highway name, [4]length, [5]speed limit
def reconstructPath(closedList):
    token = []
    parrent = closedList[-1][0]
    miles = 0

    tmp = []
    while True:
        for city in closedList:
            if city[0] == parrent:
                node = city
                break
        
        #Found start
        if(node[2] == 0):
            break
                    # city name, highway name + " for " + length + " miles"
        token.append((node[0],str(node[3])+" for "+ str(node[4]) +" miles")) 
        parrent = node[1]
        miles += node[4]
                    #length, speedlimit
        tmp.append((node[4], node[5]))

    hours = 0
    dhours = 0
    for length, speedlim in reversed(tmp):
        tRoad = length / speedlim
        if speedlim < 50:
            dhours += tRoad
        else: 
            dhours += tRoad + 2 * np.tanh(length/1000)*(tRoad + hours)
        hours += tRoad

        
    return list(reversed(token)), float(miles), hours, dhours


def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    #roadDict {"City Name" : [ ("Next city", (int)length, (int)speed limit, "Highway Name") ...]  }
    roadDict = DictDuplicateKeys()
    roadSegments = open('./road-segments.txt', 'r').readlines()
    for index in range(len(roadSegments)):
        tmp = roadSegments[index].split()
        roadDict[tmp[0]] = (tmp[1], int(tmp[2]), int(tmp[3]), tmp[4])
        roadDict[tmp[1]] = (tmp[0], int(tmp[2]), int(tmp[3]), tmp[4])
    roadSegments.clear() #don't need anymore

    #gpsDict {"City Name" : ((float)latitude, (float)longitude,)  }
    gpsDict = {}
    cityGps = open('./city-gps.txt', 'r').readlines()
    for str in cityGps:
        tmp = str.split()
        gpsDict[tmp[0]] = np.array([float(tmp[1]), float(tmp[2])])
    cityGps.clear() #don't need anymore

    endLatLon = gpsDict[end]
    #approximate direction, only be used if current node is not in city-gps.txt 
    direction = get_bearing(gpsDict[start][0],gpsDict[start][0], gpsDict[end][0], gpsDict[end][1])
   

    openList = queue.PriorityQueue()
    closedList = []

                #[0]:   F(n),                                    
    startNode = (heuristic(gpsDict[start], gpsDict[end]), 
                #[1]:   [0]city name, [1]parent, [2]G(n), [3]highway name, [4]length, [5]speed limit
                [start, "", 0, "", 0, 0])
    openList.put_nowait(startNode)
    
    ##############
    # A* Search
    ##############
    while(openList.qsize() > 0):
        current = openList.get() #pop node with smallest F(n)
        closedList.append(current[1]) # add it to closed List

        currCity = current[1][0]
        currG = current[1][2]

        #Found the goal
        if currCity == end: break

        #Get neighbours from road dictionary
        nearCites = roadDict[currCity]
        #city
        #[0]City name  [1]Road length, [2]Speed limit, [3]Highway Name
        for city in nearCites:
            #already in the closed list -> skip
            if any(city[0] == node[0] for node in closedList):
                continue

            #G(city) = G(current) + G(current, city)
            if cost == "segments": G = currG + 1000
            elif cost == "distance": G = currG + city[1]
            elif cost == "time": G = currG + 55 * city[1]/city[2]
            elif cost == "delivery":
                if city[2] < 50:
                    G = currG +  55 * city[1]/city[2]
                else: 
                    G = currG +  55* city[1]/city[2] + 2 * 55 * np.tanh(city[1]/1000)*(city[1]/city[2] + currG)

            #already in the open List & G is larger(worse) than exist one -> skip
            if any(city[0] == node[1][0] and G > node[1][2] for node in openList.queue):
                continue

            if city[0] in gpsDict:
                h = heuristic(gpsDict[city[0]], endLatLon)
            #lat/lon not found, approximation needed
            else:              #endLat/Lon, direction, length of highway, cityname, parrentLat/Lon, gpsDict
                h = heuristic2(endLatLon, direction, city[1]*2/3, city[0], gpsDict[currCity], gpsDict)
                                    #F(n),      city name , parent, G(n), highway name, length, speed

            #put neighbour city in openList
            openList.put_nowait( ( G+h,    [city[0], currCity, G, city[3], city[1], city[2]]   ) ) 
    ##############
    
    route_taken, miles, hours, dhours = reconstructPath(closedList)
    return {"total-segments" : len(route_taken), 
            "total-miles" : miles, 
            "total-hours" : hours, 
            "total-delivery-hours" : dhours, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


