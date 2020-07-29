# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint
from bson.son import SON

# establing connection
try:
    connect = MongoClient('localhost', 27017)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

mydb = connect["tracerouteDB"]
mycol = mydb["traces"]

#mycol.drop()

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

#return the distinct ASNs
for asn in mycol.distinct("Tracert.ASN"):
	print(asn)

# for x in mycol.find():
# 	pprint(x)
# 	break


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

