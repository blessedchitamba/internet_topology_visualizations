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
adjlist = []  #list of lists. each element is a list containing [source, [list of destinations]]
count=0
vertices=[]  #list of all unique vertices to use to check the existence of a vertex before adding it as a duplicate
uniqueNodes = []  #list of all unique nodes
for x in mycol.find():
	#source is a list variable with ASN and City
	#source = [x['ProbeInfo']['ASN'], x['City']]	

	if len(x['Tracert'])!=0:
		source = [x['Tracert'][0]['ASN'], x['Tracert'][0]['City']]
	else:
		continue

	#iterate through every element in the document's Tracert array checking set number
	for a in x['Tracert']:

		#first check if source does not have empty ASN or City
		if source[0]=='' or source[1]=='' or source[1]==None:
			source = [a['ASN'], a['City']]
			continue

		#first check if ASN='' or City=''
		if a['ASN']=='' or a['City']=='' or a['City']==None:
			continue

		#destination is a list variable
		destination = [a['ASN'], a['City']]
		#keep updating the destination variable until the ASN and City is different from source
		if source==destination:
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

		#to ensure first source node of iteration is not left out
		if source not in uniqueNodes:
			uniqueNodes.append(source)

		#exchange the variables
		source = destination
		#to ensure end destination nodes are not left out
		if source not in uniqueNodes:
			uniqueNodes.append(source)
	
	
#write the adjacency lists
# with open('asn_nodesAndLinks.csv', mode='w', newline='') as csv_file:
# 	    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# 	    csv_writer.writerow(['#Data format: Vertex ASN and City, Connections'])
# 	    for vertex in adjlist:
# 	    	csv_writer.writerow(vertex)

#write the unique nodes
f = open("uniqueNodes.txt", "w", newline='\n')
for node in uniqueNodes:
	f.write(str(node[0])+","+str(node[1]))
	f.write('\n')
	count+=1
f.close()
print("unique nodes written:",count)


#class for node
class Node:
  def __init__(IP, setNumber):
    self.IP = IP
    self.setNumber = setNumber
  