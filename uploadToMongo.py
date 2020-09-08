# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint
import geoip2.database

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

# with open("nullSetNumber.json") as json_file:
#     data = json.load(json_file)

#     #each traceroute hop is an individual document. 
#     for testResult in data["Results"]:
#         old_col.insert_one(testResult)

# #delete all tracert elements with null IP
# qu = {}
# update = { "$pull": { "Tracert": { "IP": "" } } }
# result = old_col.update_many(qu, update, upsert=True)
# print("Number of documents matched and modified: ", result.matched_count, result.modified_count)

# Printing the data inserted
cursor = old_col.find()
for record in cursor:
    pprint(record)
    #break


# directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/ripe_data'
# # This creates a Reader object. You should use the same object
# # across multiple requests as creation of it is expensive.
# pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-ASN_20200721/GeoLite2-ASN.mmdb"
# pathToCityDB = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"

# with geoip2.database.Reader(pathToDb) as reader:
#     with geoip2.database.Reader(pathToCityDB ) as cityReader:
#         for filename in os.listdir(directory):
#             a = filename
#             with open("../ripe_data/"+a) as json_file:
#                 data = json.load(json_file)

#                 #add this before each sequence of traceroute hop documents to indicate the start of a set of traces.
#                 source_address = { "source_address": data['src_addr'] }
#                 ripe_collection.insert_one(source_address)

#                 #each traceroute hop is an individual document. 
#                 for testResult in data["result"]:

#                     #first discard any testResult that has empty traces
#                     if testResult['result'][0]=={'x': '*'}:
#                         continue

#                     ip = testResult['result'][0]['from']

#                     try:
#                         response = reader.asn(ip)
#                         cityResponse = cityReader.city(ip)
#                         asn = response.autonomous_system_number
#                         city= cityResponse.city.name
#                     except:
#                         print("Address not in database")
#                         asn = ""
#                         city = ""

#                     #append the new fields to the testResult
#                     testResult.update({"ASN": asn})
#                     testResult.update({"City": city})
#                     ripe_collection.insert_one(testResult)

# with open("trace/trace2fdb8035-b44c-4aa0-9c9e-7dce0449cc25.txt") as json_file:
#     data = json.load(json_file)
#     collection.insert_one(data)

# # Printing the data inserted
# cursor = ripe_collection.find()
# for record in cursor:
#     pprint(record)
#     #break

