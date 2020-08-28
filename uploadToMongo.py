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
#collection = db.traces
ripe_collection = db.ripe_traces

directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/ripe_data'
for filename in os.listdir(directory):
    a = filename
    with open("../ripe_data/"+a) as json_file:
        data = json.load(json_file)
        for testResult in data["result"]:
            ripe_collection.insert_one(testResult)

# with open("trace/trace2fdb8035-b44c-4aa0-9c9e-7dce0449cc25.txt") as json_file:
#     data = json.load(json_file)
#     collection.insert_one(data)

# Printing the data inserted
cursor = ripe_collection.find()
for record in cursor:
    pprint(record)
    break

