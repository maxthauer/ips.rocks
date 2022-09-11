#!/usr/bin/python3
from flask import *
from flask_sslify import SSLify
import json, geoip2.database, ipaddress
from datetime import datetime
import logging
import google.cloud.logging

client = google.cloud.logging.Client()
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
		latitude = longitude = country = state = city = network = asn = org = 'N/A'
		return latitude, longitude, country, state, city, network, asn, org

app = Flask(__name__)
#sslify = SSLify(app)
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
		network = str(lookup[5])
		asn = lookup[6]	
		org = lookup[7]
		#dt = datetime.now()
		dt = int(datetime.now().timestamp())
		logentry = ("#iplocation#|{}|{}|GET|/".format(dt,clientip))
		logger = client.logger(logentry)
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
		network = str(lookup[5])
		asn = lookup[6]	
		org = lookup[7]
		dt = int(datetime.now().timestamp())
		logentry = ("#iplocation#|{}|{}|GET|/".format(dt,clientip))
		logger = client.logger(logentry)
		return jsonify({"query": clientip, "country": country, "latitude": latitude, "longitude": longitude, "province/state": state, "city": city, "network": network, "asn": asn, "org": org}), 200

@app.route('/api/', methods=['GET'])
def api():
	ip = request.args['ip']
	ip = str(ip)
	if request.headers.getlist("X-Forwarded-For"):
		sourceip = request.headers.getlist("X-Forwarded-For")[0]
	else:
		sourceip = request.remote_addr
	try:
		clientip = ipaddress.ip_address(ip)
		lookup = geoiplookup(clientip)
		clientip = str(clientip)
		latitude = lookup[0]
		longitude = lookup[1]
		country = lookup[2]
		state = str(lookup[3])
		city = str(lookup[4])
		network = str(lookup[5])
		asn = lookup[6]	
		org = str(lookup[7])
		dt = int(datetime.now().timestamp())
		logentry = ("#iplocation#|{}|{}|GET|/api/?ip={}".format(dt,sourceip,ip))
		logger = client.logger(logentry)
		return jsonify({"query": clientip, "country": country, "latitude": latitude, "longitude": longitude, "province/state": state, "city": city, "network": network, "asn": asn, "org": org}), 200
	except:
		dt = int(datetime.now().timestamp())
		logentry = ("#iplocation#|{}|{}|GET|/api/?ip={}".format(dt,sourceip,ip))
		logger = client.logger(logentry)
		return jsonify({"error": "Please enter an IP address", "example": "https://ips.rocks/api/?ip=8.8.8.8"}), 500

@app.route('/plain', methods=['GET'])
def plain():
	if request.headers.getlist("X-Forwarded-For"):
		clientip = request.headers.getlist("X-Forwarded-For")[0]
		clientip = clientip.split(",")
		clientip = clientip[0]
		dt = int(datetime.now().timestamp())
		#print (clientip)
		logentry = ("#iplocation#|{}|{}|GET|/plain".format(dt,clientip))
		logger = client.logger(logentry)
		return (clientip)
	else:
		clientip = request.remote_addr
		clientip = clientip.split(",")
		clientip = clientip[0]
		dt = int(datetime.now().timestamp())
		logentry = ("#iplocation#|{}|{}|GET|/plain".format(dt,clientip))
		logger = client.logger(logentry)
		return (clientip)

@app.route('/time', methods=['GET'])
def time():
	epoch = int(datetime.now().timestamp())
	return jsonify(epoch), 200

if __name__ == '__main__':
  #app.run(host='0.0.0.0', debug=False, use_reloader=False, port=443)
  app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
