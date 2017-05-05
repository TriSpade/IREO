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
	
        i = 1
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
		print(i)
		print(ibmData)
		i = i+1

		time.sleep(DELAY - (end_time-start_time))

def publish_csv(row):
	
	parsed_row = row

	timestamp = datetime.datetime.strptime(parsed_row[1],"%Y/%m/%d %H:%M:%S")

	temperature = str(parsed_row[2])
	conductivity = str(parsed_row[3])
	ph = str(parsed_row[4])
	depth = str(parsed_row[5])
	turbidity = str(parsed_row[6])
	do_sat = str(parsed_row[7])
	do_mgl = str(parsed_row[8])
	cablepowerv = str(parsed_row[9])
	latitude = str(parsed_row[11])
	longitude = str(parsed_row[12])
	
	geolookup = getGeolocation(latitude,longitude)
	
	date = timestamp.strftime("%Y%m%d")
	state = geolookup['location']['state']
	city = geolookup['location']['city']

	#print("This sensor is located in %s, %s, %s" % (city,state,timestamp),)

	dailyWeather = getWeather(state,city,date)
	meantempm = dailyWeather[0]["meantempm"]
	meanprecip = dailyWeather[0]["precipm"]

	if meanprecip == "T":
		meanprecip = "0.0";

	#ibmData = '{"d" : {"temperature" : "'+temperature+'" , "conductivity" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "turbidity" : "'+turbidity+'" , "do_sat" : "'+do_sat+'" , "do_mgl" : "'+do_mgl+'" , "cablepowerv" : "'+cablepowerv+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'" , "meanpercip" : "'+meanpercip+'" "} }'
	ibmData = '{"d" : {"temp" : "'+temperature+'" , "cond" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "tur" : "'+turbidity+'" , "dosat" : "'+do_sat+'" , "domgl" : "'+do_mgl+'" , "power" : "'+cablepowerv+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'" , "precipm" : "'+meanprecip+'" } }'

	deviceClient.publishEvent("status", "json", ibmData);
	
	print(ibmData)

		

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

cur.execute("SELECT * FROM `observations` Limit 411")

publish(cur.fetchall())

cur.close()

with open('SRBwaterquality_Outliers.csv') as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	count = 0
	for row in csvReader:
		start_time = time.time()
		publish_csv(row)
		end_time = time.time()
		print("the last entry was: " + str(count))
		count = count + 1;
		time.sleep(DELAY)


