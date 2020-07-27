import geoip2.database
# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint

# establing connection
try:
    connect = MongoClient('mongodb://localhost:27017/')
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.tracerouteDB

# creating or switching to demoCollection
collection = db.traces



# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-ASN_20200721/GeoLite2-ASN.mmdb"
with geoip2.database.Reader(pathToDb) as reader:
	#iterate through each document's Tracert array
	ip = ""
	asn = ""
	tracerts = []
	for x in collection.find():
		for trace in x['Tracert']:
			ip = trace['IP']
			try:
				response = reader.asn(ip)
				asn = response.autonomous_system_number
			except:
				print("Address not in database")
				asn = ""
			qu = {}
			update = {"$set": {"Tracert.$[inner].ASN": asn}}
			filter = [{"inner.IP": ip}]
			collection.update_many(qu, update, upsert=True, array_filters=filter)
			#print(ip, response.autonomous_system_number)
			