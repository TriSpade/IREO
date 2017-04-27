/*eslint-env node*/

//------------------------------------------------------------------------------
// node.js starter application for Bluemix
//------------------------------------------------------------------------------

// This application uses express as its web server
// for more info, see: http://expressjs.com
var express = require('express');
var request = require('request');

_ = require('lodash');
// cfenv provides access to your Cloud Foundry environment
// for more info, see: https://www.npmjs.com/package/cfenv
var cfenv = require('cfenv');

// create a new express server
var app = express();

// serve the files out of ./public as our main files
app.use(express.static(__dirname + '/public'));

// get the app environment from Cloud Foundry
var appEnv = cfenv.getAppEnv();

var mysql = require("mysql");
var Client = require('ibmiotf');

var async = require('asyncawait/async');
var await = require('asyncawait/await');

// First you need to create a connection to the db
var con = mysql.createConnection({
  host: "webofagents.cs.clemson.edu",
  user: "sim_app",//sim_app
  password: "irviewer",
  database: "intelligentriver"
});

con.connect(function(err){
  if(err){
    console.log('Error connecting to Db');
    return;
  }
  console.log('Connection established');
});


var config = {
    "org" : "vh3t8t",
    "id" : "8649865433",
    "domain": "internetofthings.ibmcloud.com",
    "type" : "InteliRiver",
    "auth-method" : "token",
    "auth-token" : "8649865433"
};
var deviceClient = new Client.IotfDevice(config);

deviceClient.connect();

var rows =[];

function getWeather(latitude, longitude, startDate, endDate) {
   // Prepare output in JSON format
		let callURL = "https://d8d775bd-d009-4709-b9f5-e0da76a5ebc6:ukxwFlxUKf@twcservice.mybluemix.net/api/weather/v1/geocode/"+latitude+"/"+longitude+"/almanac/daily.json?units=e&start="+startDate+"&end="+endDate

    	request.get(callURL, {'json': true}, function(err,response,body){
      			if(err){
					console.log(err);
				} else {
					//console.log(body);
					return body;
				}
    	});                     
};

var i=0;
var previous_system_time = 0;
var previous_database_time = 0;


var publish = async(function(rows){
	
	    var timestamp = rows[i].timestamp;
		var motestack = rows[i].motestack;   
		var temperature = rows[i].temperature;
		var spcond = rows[i].spcond;
		var ph = rows[i].ph;   
		var depth = rows[i].depth;
		var power = rows[i].power;   
		var turbidity = rows[i].turbidity;
		var piezoresistance = rows[i].piezoresistance
		var mgl_odo_sat = rows[i].mgl_odo_sat
		var longitude = "-82.49357"
		var latitude = "34.5244887"
		var startDate = "0312"
		var endDate = "0312"

		var weatherData = await(getWeather(latitude, longitude, startDate, endDate));
    	console.log(weatherData);
		
		//deviceClient.publish('Device { "time" : \"'+timestamp+'\" , "mote" : \"'+motestack+'\" , "temp" : \"'+temperature+'\" , "spcond" : \"'+spcond+'\" , "ph" : \"'+ph+'\" , "depth" : \"'+depth+'\" , "turbidity" : \"'+turbidity+'\", "power" : \"'+power+'\" , "piezoresistance" : \"'+piezoresistance+'\" , "mgl_odo_sat" : \"'+mgl_odo_sat+'\", "latitude" : \"'+latitude+'\", "longitude" : \"'+longitude+'\" }');
		//console.log('Device { "time" : \"'+timestamp+'\" , "mote" : \"'+motestack+'\" , "temp" : \"'+temperature+'\" , "spcond" : \"'+spcond+'\" , "ph" : \"'+ph+'\" , "depth" : \"'+depth+'\" , "turbidity" : \"'+turbidity+'\", "power" : \"'+power+'\" , "piezoresistance" : \"'+piezoresistance+'\" , "mgl_odo_sat" : \"'+mgl_odo_sat+'\", "latitude" : \"'+latitude+'\", "longitude" : \"'+longitude+'\" }');
		i=i+1;  
});
	

deviceClient.on('connect', function () {

console.log("Device Connected")

con.query('SELECT * FROM `observations` WHERE `timestamp` >= \'2016-01-06 00:00:00\' ORDER BY `timestamp` ASC',function(err,sqlrows){
     if(err) throw err;
	 rows = sqlrows;
	console.log('Data received from Db:\n');
    setInterval(publish,1000,rows);


  });
  con.end(function(err) {
  // The connection is terminated gracefully
  // Ensures all previously enqueued queries are still
  // before sending a COM_QUIT packet to the MySQL server.
  });

//});

	
});

deviceClient.on("error", function (err) {
    console.log("Error : **************************************************************************************************************************************************"+err);
});