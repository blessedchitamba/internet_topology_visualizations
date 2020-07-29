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

f = open('midar-83.sets','r')
#loop through file and discard the first 6 lines beginning with hash
for line in f:
	if line[0:1]=='#':
		continue
	else:
		break

lineCount =0
ip=""
for line in f:
	if line[0:1]=='#':
		lineCount+=1
	else:
		ip = line.strip()
		#filter = {"TracerouteTestResults.Tracert.IP": ip}
		#update = {'$set': {'status' : 'posted'}}

		#update the probe info object (the outside)
		#query = {"TracerouteTestResults.IP": ip}
		#update = {"$set":{"TracerouteTestResults.set":lineCount}}
		#collection.update_many(query,update)
		# query = {"TracerouteTestResults.Tracert":{"$elemMatch":{"IP":ip}}}
		# update = {"$set":{"TracerouteTestResults.Tracert.set":lineCount}}
		# collection.update_many(query,update)

		qu = {}
		update = {"$set": {"Tracert.$[inner].setNumber": lineCount}}
		filter = [{"inner.IP": ip}]
		collection.update_many(qu, update, upsert=True, array_filters=filter)

		qu = {"IP": ip}
		update = {"$set": {"setNumber": lineCount}}
		collection.update_many(qu, update)


# Printing the data inserted
cursor = collection.find()
#cursor = collection.find({"CountryCode": "EG"})
for record in cursor:
    pprint(record)
    #break
