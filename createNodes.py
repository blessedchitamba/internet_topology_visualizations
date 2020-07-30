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
from array import *
import csv

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
adjlist = []
count=0
vertices=[]
for x in mycol.find():
	#check if document has set attribute
	source = x['ProbeInfo']['ASN']
	count+=1
	

	#iterate through every element in the document's Tracert array checking set number
	for a in x['Tracert']:
		#first check if ASN=''
		if a['ASN']=='':
			continue

		destination = a['ASN']
		#keep updating the destination variable until the ASN is different from source
		if source==destination:
			#destination = a['ASN']
			continue

		#once it gets to this if it means source!=destination
		if source not in vertices:
			temp=[]
			temp.append(source)
			vertices.append(source)
			temp.append(destination)
			adjlist.append(temp)
			#print(adjlist)
		else:
			index = vertices.index(source)
			if destination not in adjlist[index]:
				adjlist[index].append(destination)
		#print(str(source)+": "+str(destination))

		#exchange the variables
		source = destination
	

with open('asn_nodesAndLinks.csv', mode='w', newline='') as csv_file:
	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    csv_writer.writerow(['#Data format: Vertex ASN, Connections'])
	    for vertex in adjlist:
	    	csv_writer.writerow(vertex)

#class for node
class Node:
  def __init__(IP, setNumber):
    self.IP = IP
    self.setNumber = setNumber
  