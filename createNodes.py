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

#array with size=number of alias sets; we will use it to indicate with a 0 or 1 whether a particular alias set has an adjacency list or not
checkArray = [0]*100

for x in mycol.find():
  #check if document has set attribute
  sourceIP = x['IP']
  #the previous (IP, set) combination is kept and is initially set to the source IP
  previousNode = Node(sourceIP, x['setNumber'])
  #iterate through every element in the document's Tracert array checking set number
  for a in x['Tracert']:
  	#first check if set number is -1
  	if a['setNumber']==-1:
  		#that IP is unique; be careful though because an IP might appear in more than one trace
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

print("over")

#class for node
class Node:
  def __init__(IP, setNumber):
    self.IP = IP
    self.setNumber = setNumber
  