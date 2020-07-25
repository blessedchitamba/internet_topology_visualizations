"""
-Go through each document, check if the IP attribute has a corresponding setNumber (the host IP router)
-If set number exists, take the IP and setNumber (null if it doesn’t) and add them to an adjacency list db as a single starting vertex instance. 
 In the Tracert array, add the first entry to the adjacency list as a connection
-Iterate through the document's Tracert array and for every other traceroute instance create an adjacency list for it and add the next instance. 
 First check though if no adjacency list has been made already for that set number. Use an array that will indicate 0 or 1 depending on whether 
 that set has a list or not.
-Do the same for every document
-Write the adj list in a csv file
"""

# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint

# establing connection
try:
    connect = MongoClient('localhost', 27017)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

mydb = connect["tracerouteDB"]
mycol = mydb["traces"]

for x in mycol.find():
  #check if document has set attribute
  sourceIP = x['IP']
  #the previous (IP, set) combination is kept and is initially set to the source IP
  previousNode = Node(sourceIP, a[setNumber])
  for a in x['Tracert']:
  	try:
  		if checkArray[a['setNumber']]==0:
  			#means adjacency ist is not made yet for this set
  			createAdjacency(a['IP'], a[setNumber])
  			checkArray[a[setNumber]]+=1
  			#add this current instance of node to the previous node's adjacency list
  			addToAdjacency(previousNode, a['IP'], a[setNumber])


  		else:
  			#add it as an adjacency listi
  			addToAdjacency(previousNode, a['IP'], a[setNumber])
  		previousNode = makeNode(a['IP'], a[setNumber])


  		pprint(a['setNumber'])
  	except:
  		continue

print("over")

#class for node
class Node:
  def __init__(IP, setNumber=-1):
    self.IP = IP
    self.setNumber = setNumber
  