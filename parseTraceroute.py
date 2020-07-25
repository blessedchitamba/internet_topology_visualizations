import json
import os

directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/code/trace'
f = open("ips.txt", "w", newline='')
for filename in os.listdir(directory):
	a = filename
	with open("trace/"+a) as json_file:
	    data = json.load(json_file)
	    print ("ResponseStatus:", data['ResponseStatus'])
	    print ("")
	    for probeResult in data['TracerouteTestResults']:
	    	print("ProbeInfo:", probeResult['ProbeInfo']['ASN'])
	    	print("Destination IP:", probeResult['IP'])
	    	f.write(probeResult['IP'].strip())
	    	f.write('\n')
	    	for tracert in probeResult['Tracert']:
	    		if tracert['IP']:
	    			print("IP:", tracert['IP'])
	    			f.write(tracert['IP'].strip())
	    			f.write('\n')
	    	print("")
        