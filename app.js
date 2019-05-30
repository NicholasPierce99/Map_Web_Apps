//module for sqlite3
var sqlite3 = require('sqlite3').verbose();

//establish connection to sqlite database
let db = new sqlite3.Database('./db/locationBase.db');


//module that makes sure to include specific functions, in this case express
var express = require('express');

//includes bodyparser for form data
const bodyParser = require("body-parser");


//express framework for handling request payloads
var app = express();

//uses standard url based forms

//use express bodyparser to convert data to json objects
app.use(bodyParser.json());

//allows for non encrypted data to be sent through browsers
app.use(bodyParser.urlencoded({
  extended: true
}));


//get request for file in root directory and sub html directory
app.get('/', function(req, res) {
	res.sendFile(__dirname + '/html/indexJS.html');
});
//makes post request for contents of latitude and longitude to save to sqlite3 db
app.post('/', function(req, res) {
	
	//node handles all post requests using bodyParser and converts them to elements of a json
	var latitude = req.body.latitude;
	var longitude = req.body.longitude;
	
	latitude = parseFloat(latitude);
	longitude = parseFloat(longitude);
	
	db.run('insert into latitudeLongitude (latitude)  values (?)', [latitude]);
	db.run('insert into latitudeLongitude (longitude)  values (?)', [longitude]);
	
	res.redirect('/');
});

app.get('/visited', function(req, res) {

  let sql = 'select * from latitudeLongitude';
  db.all(sql, [], (err, rows) => {
  
  rows.forEach((row) => {
    console.log(row);
  });
  });
	
	res.redirect('/')
	
});

//specify port to listen to by web application
//127.0.0.1 loopback
app.listen(8080);

console.log("listening on 8080!");
