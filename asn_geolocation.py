import geoip2.database
# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint
import csv

# establing connection
try:
    connect = MongoClient('mongodb://localhost:27017/')
    #print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.tracerouteDB

# creating or switching to demoCollection
collection = db.traces

#read the file with the asns and find each corresponding IP and geolocate it
f = open("uniqueAsn.txt", "r")
f.readline()

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"
with geoip2.database.Reader(pathToDb) as reader:
	with open('asn_nodes_raw.csv', mode='w', newline='') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(['IP', 'ASN', 'Longitude', 'Latitude'])
	    for line in f:
	    	for x in collection.find({"Tracert.ASN": int(line.strip())}, {"Tracert": {"$elemMatch": {"ASN": int(line.strip())}}}):
	    		response = reader.city(x['Tracert'][0]['IP'])
	    		csv_writer.writerow([x['Tracert'][0]['IP'], x['Tracert'][0]['ASN'], response.location.longitude, response.location.latitude])
	    		#pprint(x['Tracert'][0]['ASN'])
	    		break

#close file
f.close()

