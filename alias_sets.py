from pymongo import MongoClient
import geoip2.database
import json
import os
import csv
import pandas as pd
from pprint import pprint


def update_mongo_with_alias_set(platform):
    # establing connection
    try:
        connect = MongoClient('mongodb://localhost:27017/')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    # creating or switching to demoCollection 
    #collection = db.traces
    #ripe_collection = db.ripe_traces
    old_col = db.old_speedchecker_collection

    f = open('midar-83.sets', 'r')
    # loop through file and discard the first 6 lines beginning with hash
    for line in f:
        if line[0:1] == '#':
            continue
        else:
            break

    setCount = 0
    ip = ""
    bloom_filter = [0]*65   #array to check 0 or 1 whether set number has a node yet
    # This creates a Reader object. You should use the same object
    # across multiple requests as creation of it is expensive.
    pathToCityDB = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"

    with geoip2.database.Reader(pathToCityDB ) as cityReader:
        with open('router_locations.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['IP', 'Set_Num', 'Longitude', 'Latitude'])
            for line in f:
                if line[0:1] == '#':
                    setCount += 1
                elif bloom_filter[setCount]==1:
                    #set already has a node
                    continue
                else:
                    #get the IP on that line and try to geolocate it
                    ip = line.strip()
                    if platform == "SpeedChecker":
                        try:
                            response = cityReader.city(ip)
                            longitude = response.location.longitude
                            latitude = response.location.latitude
                            bloom_filter[setCount] = 1

                            #write the node to the file
                            csv_writer.writerow([ip, setCount, longitude, latitude])
                        except:
                            print("Address not in database")
                            

                    elif platform == "CAIDA":
                        # havent thought about it yet
                        print("not yet")

                    elif platform == "RIPE":
                        # think about it later
                        print("not yet")

            #now go for those ips in the database that have -1 set number
            cursor = old_col.distinct("Tracert.IP")
            for ip in cursor:
                try:
                    response = cityReader.city(ip)
                    longitude = response.location.longitude
                    latitude = response.location.latitude

                    #write the node to the file
                    csv_writer.writerow([ip, -1, longitude, latitude])
                except:
                    print("Address not in database")

    connect.close()
    #os.remove("files/midar.sets")


def clean_db(platform):
    # establing connection
    try:
        connect = MongoClient('mongodb://localhost:27017/')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    # creating or switching to demoCollection 
    #collection = db.traces
    #ripe_collection = db.ripe_traces
    old_col = db.old_speedchecker_collection

    # This creates a Reader object. You should use the same object
    # across multiple requests as creation of it is expensive.
    pathToCityDB = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"

    with geoip2.database.Reader(pathToCityDB ) as cityReader:

        #select appropriate platform
        if platform == "SpeedChecker":
            # iterate through each document's Tracert array
            count = 0
            for x in old_col.find():

                #first add city to the Probe Info
                probeIP = x['IP']
                try:
                    cityResponse = cityReader.city(probeIP)
                    lat = cityResponse.location.latitude
                    long = cityResponse.location.longitude
                except:
                    print("Address not in database")
                    lat = ""
                    long = ""
                qu = {"IP": probeIP}
                update = {"$set": {"Latitude": lat,
                                   "Longitude": long}}
                old_col.update_many(qu, update, upsert=True)

                #go through each IP, try geolocate it, add null if its not in the db
                for trace in x['Tracert']:
                    ip = trace['IP']
                    try:
                        cityResponse = cityReader.city(ip)
                        lat = cityResponse.location.latitude
                        long = cityResponse.location.longitude
                    except:
                        print("Address not in database")
                        lat = ""
                        long = ""
                    qu = {}
                    update = {"$set": {"Tracert.$[inner].Latitude": lat,
                                       "Tracert.$[inner].Longitude": long}}
                    filter = [{"inner.IP": ip}]
                    old_col.update_many(qu, update, upsert=True, array_filters=filter)
        elif platform == "CAIDA":
            # havent thought about it yet
            # fetch data from 
            print("not yet")

        elif platform == "RIPE":
            print("not yet")

    #delete all ips with no geolocation
    qu = {}
    update = { "$pull": { "Tracert": { "Longitude": "" } } }
    result = old_col.update_many(qu, update, upsert=True)
    print("Number of documents matched and modified: ", result.matched_count, result.modified_count)
    connect.close()

def create_router_links(platform):
    # establing connection
    try:
        connect = MongoClient('mongodb://localhost:27017/')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    # creating or switching to demoCollection 
    #collection = db.traces
    #ripe_collection = db.ripe_traces
    old_col = db.old_speedchecker_collection

    sources = []
    targets = []
    adjlist = []  #list of lists. each element is a list containing [source, [list of destinations]]
    if platform == "SpeedChecker":
        for x in old_col.find():

            if len(x['Tracert'])!=0:
                source = x['Tracert'][0]['IP']
                source_longLat = [x['Tracert'][0]['Longitude'], x['Tracert'][0]['Latitude']]
            else:
                continue

            # iterate through every element in the document's Tracert array checking set number
            for a in x['Tracert']:

                #destination is a list variable
                destination = a['IP']
                dest_longLat = [a['Longitude'], a['Latitude']]
                # keep updating the destination variable until the ASN is different from source
                if source_longLat == dest_longLat:
                    continue

                # #append rtt to source and destination
                # total = 0
                # if a['PingTimeArray']!=None:
                #     for rtt in a['PingTimeArray']:
                #         total += int(rtt)
                #     avg_rtt = round(total/len(a['PingTimeArray']), 2)
                # else:
                #     avg_rtt=0.0

                sources.append(source)
                targets.append(destination)
                temp=[]
                temp.append(source)
                temp.append(destination)
                #temp.append([avg_rtt])
                adjlist.append(temp)

                #exchange the variables
                source = destination

    elif platform == "CAIDA":
        # havent thought about it yet
        print("not yet")

    elif platform == "RIPE":
        # think about it later
        print("not yet")

    #write the adjacency lists
    with open('router_source_destination.csv', mode='w', newline='') as csv_file:
          csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          csv_writer.writerow(["Source_IP", "Target_IP"])
          for link in adjlist:
              csv_writer.writerow([str(link[0]), str(link[1])])
    print("done and stored asn_source_destination in csv file")
    connect.close()


if __name__ == '__main__':
    #update_mongo_with_alias_set("SpeedChecker")
    #clean_db("SpeedChecker")
    create_router_links("SpeedChecker")