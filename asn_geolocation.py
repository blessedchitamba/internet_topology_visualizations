import geoip2.database
# importing pymongo
from pymongo import MongoClient
import json
import os
from pprint import pprint
import csv
import random

# establing connection
try:
	connect = MongoClient('mongodb://localhost:27017/')
	#print("Connected successfully!!!")
except:
	print("Could not connect to MongoDB")

# connecting or switching to the database
db = connect.tracerouteDB

# creating or switching to demoCollection
collection = db.traces

#function to calculate an average geolocation of many ips
def avg_ip(ips, reader):
	totalLong = 0
	totalLat = 0
	for ip in ips:
		response = reader.city(ip)
		totalLong += response.location.longitude
		totalLat += response.location.latitude
	return [totalLong/len(ips), totalLat/len(ips)]

#function to calculate an average geolocation of many ips
def get_geoloc(ips, reader,lis):
	response = reader.city(ips)
	Long = response.location.longitude
	Lat = response.location.latitude
	if Lat in lis or Long in lis:
		Long+=2
		Lat+=2
	return [Long,Lat]



#read the file with the asns and find each corresponding IP and geolocate it
f = open("uniqueNodes.txt", "r")

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
pathToDb = "C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-City_20200721/GeoLite2-City.mmdb"
lis = []
with geoip2.database.Reader(pathToDb) as reader:
	with open('asn_locations.csv', mode='w', newline='') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow(['ASN', 'City', 'Longitude', 'Latitude'])
		ips = []
		data = list(collection.find({}, {"Tracert.ASN": 1, "Tracert.City":1, "Tracert.IP": 1}))
		for line in f:
			asn = int(line.split(",")[0])
			city = line.split(",")[1].strip()
			for x in data:
				# response = reader.city(x['Tracert'][0]['IP'])
				#search in the document for all IPs where city and asn are equal to the desired
				for trace in x['Tracert']:
					if trace['ASN']==asn and trace['City']==city:
						ips.append(trace['IP'])
						#print(trace['ASN'], trace['City'], trace['IP'])
			
			
			averageGeoloc = get_geoloc(ips[0], reader,lis)
			lis.append(averageGeoloc[0])
			lis.append(averageGeoloc[1])

			print("[",asn,",",city,"]",": ",averageGeoloc[0]," ", averageGeoloc[1], sep="")
			csv_writer.writerow([asn, city, averageGeoloc[0], averageGeoloc[1]])
			del ips[:]
				# csv_writer.writerow([x['Tracert'][0]['ASN'], response.location.longitude, response.location.latitude])
				#pprint(x['Tracert'][0]['ASN'])
				#break

#close file
f.close()
