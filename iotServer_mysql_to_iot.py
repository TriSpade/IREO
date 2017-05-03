#!/bin/env python

import MySQLdb
import requests
import ibmiotf.device
import datetime
import time
import urllib2
import json
import csv
from decimal import Decimal



DELAY = 1
STOP = 200

def getGeolocation(latitude, longitude):
	f = urllib2.urlopen('http://api.wunderground.com/api/8eef714101de1a6c/geolookup/q/'+latitude+','+longitude+'.json')
	json_string = f.read()

	parsed_json = json.loads(json_string)

	f.close()

	return parsed_json

def getWeather(state, city, date):
	city = city.replace(" ","_")

	url = 'http://api.wunderground.com/api/8eef714101de1a6c/history_'+date+'/q/'+state+'/'+city+'.json'

	f = urllib2.urlopen(url)
	json_string = f.read()

	parsed_json = json.loads(json_string)

	f.close()

	return parsed_json['history']['dailysummary']


def publish(row):
	
	for parsed_row in row:
		
		start_time = time.time();
		temperature = str(parsed_row[0])
		conductivity = str(parsed_row[1])
		ph = str(parsed_row[2])
		depth = str(parsed_row[3])
		turbidity = str(parsed_row[4])
		do_sat = str(parsed_row[5])
		do_mgl = str(parsed_row[6])
		cablepowerv = str(parsed_row[7])
		latitude = str(parsed_row[8])
		longitude = str(parsed_row[9])
		meantempm = str(parsed_row[10])
		meanprecip = str(parsed_row[11])

		#ibmData = '{"d" : {"temperature" : "'+temperature+'" , "conductivity" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "turbidity" : "'+turbidity+'" , "do_sat" : "'+do_sat+'" , "do_mgl" : "'+do_mgl+'" , "cablepowerv" : "'+cablepowerv+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'" , "meanpercip" : "'+meanpercip+'" "} }'
		#ibmData = json.loads('{"d" : {"temp" : "'+temperature+'" , "cond" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "tur" : "'+turbidity+'" , "dosat" : "'+do_sat+'" , "domgl" : "'+do_mgl+'" , "power" : "'+cablepowerv+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'" , "precipm" : "'+meanprecip+'" } }')
		ibmData = '{"d" : {"temp" : "'+temperature+'" , "cond" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "tur" : "'+turbidity+'" , "dosat" : "'+do_sat+'" , "domgl" : "'+do_mgl+'" , "power" : "'+cablepowerv+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'" , "precipm" : "'+meanprecip+'" } }'
		
		end_time = time.time()

		deviceClient.publishEvent("status", "json", ibmData);
	
		print(ibmData)

		time.sleep(DELAY - (end_time-start_time))
		

con = MySQLdb.connect(host= "webofagents.cs.clemson.edu",
						user= "sim_app",
						passwd= "irviewer",
						db= "IRandWeather")

print("connected to sqldb")

cur = con.cursor()



config = {
    "org" : "vh3t8t",
    "id" : "8649865433",
    "domain": "internetofthings.ibmcloud.com",
    "type" : "InteliRiver",
    "auth-method" : "token",
    "auth-token" : "8649865433"
}

try:
	deviceClient = ibmiotf.device.Client(config)
except Exception as e:
	print(str(e))
	sys.exit()

deviceClient.connect()

cur.execute("SELECT * FROM `observations`")

publish(cur.fetchall())

cur.close()


