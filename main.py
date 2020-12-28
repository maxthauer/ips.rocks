#!/usr/bin/python3
from flask import *
import json, geoip2.database

cityreader = geoip2.database.Reader('./geoip_files/GeoLite2-City.mmdb')
asnreader =  geoip2.database.Reader('./geoip_files/GeoLite2-ASN.mmdb')

def geoiplookup(clientip):
	try:
		cityresponse = cityreader.city(clientip)
		asnresponse = asnreader.asn(clientip)
		latitude = cityresponse.location.latitude
		longitude = cityresponse.location.longitude
		country = cityresponse.country.name
		state = cityresponse.subdivisions.most_specific.name
		city = cityresponse.city.name
		network = cityresponse.traits.network
		asn = asnresponse.autonomous_system_number
		org = asnresponse.autonomous_system_organization
		return latitude, longitude, country, state, city, network, asn, org
	except:
		latitude = 'N/A'
		longitude = 'N/A'
		country = 'N/A'
		state = 'N/A'
		city = 'N/A'
		network = 'N/A'
		asn = 'N/A'	
		org = 'N/A'
		return latitude, longitude, country, state, city, network, asn, org

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
	if request.headers.getlist("X-Forwarded-For"):
		clientip = request.headers.getlist("X-Forwarded-For")[0]
		try:
			clientip = clientip.split(",")
			clientip = clientip[0]
			lookup = geoiplookup(clientip)
		except:
			lookup = geoiplookup(clientip)
		latitude = lookup[0]
		longitude = lookup[1]
		country = lookup[2]
		state = lookup[3]
		city = lookup[4]
		network = lookup[5]
		asn = lookup[6]	
		org = lookup[7]
		return jsonify({"query": clientip, "country": country, "latitude": latitude, "longitude": longitude, "province/state": state, "city": city, "network": network, "asn": asn, "org": org}), 200
	else:
		clientip = request.remote_addr
		try:
			clientip = clientip.split(",")
			clientip = clientip[0]
			lookup = geoiplookup(clientip)
		except:
			lookup = geoiplookup(clientip)
		latitude = lookup[0]
		longitude = lookup[1]
		country = lookup[2]
		state = lookup[3]
		city = lookup[4]
		network = lookup[5]
		asn = lookup[6]	
		org = lookup[7]
		return jsonify({"query": clientip, "country": country, "latitude": latitude, "longitude": longitude, "province/state": state, "city": city, "network": network, "asn": asn, "org": org}), 200
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True, use_reloader=False, port=8080)


