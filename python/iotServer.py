#!/bin/env python

#import MySQLdb
import requests
import ibmiotf.device
import datetime
import time
import urllib2
import json
import csv



DELAY = 10


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
	station = str(parsed_row[10])
	latitude = str(parsed_row[11])
	longitude = str(parsed_row[12])
	
	geolookup = getGeolocation(latitude,longitude)
	
	date = timestamp.strftime("%Y%m%d")
	state = geolookup['location']['state']
	city = geolookup['location']['city']

	dailyWeather = getWeather(state,city,date)
	meantempm = dailyWeather[0]["meantempm"]
		
	ibmData = '{"timestamp" : "'+timestamp.strftime("%Y/%m/%d %H:%M:%S")+'" , "temperature" : "'+temperature+'" , "conductivity" : "'+conductivity+'" , "ph" : "'+ph+'" , "depth" : "'+depth+'" , "turbidity" : "'+turbidity+'" , "do_sat" : "'+do_sat+'" , "do_mgl" : "'+do_mgl+'" , "cablepowerv" : "'+cablepowerv+'" , "station" : "'+station+'" , "latitude" : "'+latitude+'" , "longitude" : "'+longitude+'" , "meantempm" : "'+meantempm+'}'

	deviceClient.publishEvent("status", "json", ibmData);
	print(ibmData)
		
		

#con = MySQLdb.connect(host= "webofagents.cs.clemson.edu",
#						user= "sim_app",
#						passwd= "irviewer",
#						db= "intelligentriver")

#print("connected to sqldb")

#cur = con.cursor()



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

with open('SRBwaterquality2.csv') as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	for row in csvReader:
		start_time = time.time()
		publish(row)
		end_time = time.time()
		time.sleep(DELAY - (end_time-start_time))

#cur.execute("SELECT * FROM `observations` ORDER BY `timestamp` ASC")

#publish(cur.fetchall())

#cur.close()


