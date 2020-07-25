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

directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/code/trace'
for filename in os.listdir(directory):
    a = filename
    with open("trace/"+a) as json_file:
        data = json.load(json_file)
        for testResult in data["TracerouteTestResults"]:
            collection.insert_one(testResult)

# with open("trace/trace2fdb8035-b44c-4aa0-9c9e-7dce0449cc25.txt") as json_file:
#     data = json.load(json_file)
#     collection.insert_one(data)

# Printing the data inserted
cursor = collection.find({"TracerouteTestResults.ProbeInfo.ProbeID": "1ba014c2-b7ec-4b3c-915e-f1fd7cc4327e"})
for record in cursor:
    pprint(record)
    break

