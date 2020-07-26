import geoip2.database

# This creates a Reader object. You should use the same object
# across multiple requests as creation of it is expensive.
with geoip2.database.Reader('C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/geolite_dbs/GeoLite2-ASN_20200721/GeoLite2-ASN.mmdb') as reader:
    response = reader.asn('1.128.0.0')
    print(response.autonomous_system_number)
    print(response.autonomous_system_organization)