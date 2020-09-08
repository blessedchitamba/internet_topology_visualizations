# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint
from bson.son import SON
import geoip2.database

# establing connection
try:
    connect = MongoClient('localhost', 27017)
    #print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.tracerouteDB

# creating or switching to demoCollection 
#collection = db.traces
collection = db.traces

#collection.drop()

#set all those with no set number to setNumber = -1
# qu = {}
# update = {"$set": {"Tracert.$[inner].setNumber": -1}}
# filter = [{"inner.setNumber": {"$exists": False}}]
# mycol.update_many(qu, update, upsert=True, array_filters=filter)

#delete all tracert elements with null IP
# qu = {}
# update = { "$pull": { "Tracert": { "IP": "" } } }
# result = mycol.update_many(qu, update, upsert=True)
# print("Number of documents matched and modified: ", result.matched_count, result.modified_count)

# #delete all hops with {'x': '*'} as result[0] from ripe data
# delete_query = {"result.0.x": "*"}
# result = ripe_collection.delete_many(delete_query)

#return the distinct ASNs
# for asn in collection.distinct("Tracert.ASN"):
# 	print(asn)

#return the distinct IPs
result = collection.distinct("Tracert.IP")
for ip in result:
	print(ip)
#print("Number of IPs found: ", len(result))

result = collection.distinct("IP")
for ip in result:
	print(ip)
#print("Number of IPs found: ", len(result))

# asn = 36907
# city = "Luanda"
# for x in collection.find({}, {"Tracert.ASN": 1, "Tracert.City":1, "Tracert.IP": 1}):
# 	pprint(x)
# 	#break

# for x in ripe_collection.find():
# 	pprint(x)
# 	#break


# # the list_database_names() method returns a list of strings
# database_names = connect.list_database_names()

# print ("database_names() TYPE:", type(database_names))
# print ("The client's list_database_names() method returned", len(database_names), "database names.")

# # iterate over the list of database names
# for db_num, db in enumerate(database_names):

#     # print the database name
#     print ("\nGetting collections for database:", db, "--", db_num)

#     # use the list_collection_names() method to return collection names
#     collection_names = connect[db].list_collection_names()
#     print ("list_collection_names() TYPE:", type(database_names))
#     print ("The MongoDB database returned", len(collection_names), "collections.")

#     # iterate over the list of collection names
#     for col_num, col in enumerate(collection_names):
#         print (col, "--", col_num)

# # Printing the data inserted
# cursor = collection.find({"ProbeID": "a1b44664-47a5-40ff-84e4-80cbe132a71d"})
# for record in cursor:
#     pprint(record)
#     break

