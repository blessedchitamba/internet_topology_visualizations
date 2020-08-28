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
f = open("uniqueNodes.txt", "r")

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"
with geoip2.database.Reader(pathToDb) as reader:
	with open('asn_locations.csv', mode='w', newline='') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(['ASN', 'Longitude', 'Latitude'])
	    for line in f:
	    	asn = int(line.split(",")[0])
	    	city = line.split(",")[1].strip()
	    	for x in collection.find({"Tracert.ASN": asn, "Tracert.City": city},
	    							 {"Tracert": {"$elemMatch": {"ASN": asn, "City": city}}}):
	    		# response = reader.city(x['Tracert'][0]['IP'])
	    		print(x['Tracert'][0]['ASN'], x['Tracert'][0]['City'])
	    		# csv_writer.writerow([x['Tracert'][0]['ASN'], response.location.longitude, response.location.latitude])
	    		#pprint(x['Tracert'][0]['ASN'])
	    		#break

#close file
f.close()


#function to calculate an average geolocation of many ips
def avg_ip(ips, reader):
	for ip in ips:
		response = reader.city(ip)
		longitude = response.location.longitude
		latitude = response.location.latitude
