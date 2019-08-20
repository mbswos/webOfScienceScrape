var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var fs = require('fs');
const utf8 = require('utf8');

const hostname = 'localhost';
const port = 3000;
//setup database connection
const dbhost = 'localhost';
const user = 'root';
const password = 'admin';
const database = 'webofsciencescraper';

var con = mysql.createConnection({
  host: dbhost,
  user: user,
  password: password,
  database: database,
  multipleStatements: true
});

//connect to db
con.connect(function(err){
  if(err) throw err;
  console.log('Connected!')
});

//setup sql
var publications_query = fs.readFileSync('./database_scripts/DepartmentsAndPublications.sql', 'utf8');
var ratemyprofessors_query = fs.readFileSync('./database_scripts/DepartmentsAndRateMyProfessors.sql', 'utf8');
var googlescholar_query = fs.readFileSync('./database_scripts/DepartmentsAndGoogleScholar.sql', 'utf8');
var departments_query = fs.readFileSync('./database_scripts/Departments.sql', 'utf8');

router.get('/publications.json', function(req, res, next) {
	con.query(publications_query, function(err, result){
		for(r of result[1]){
			if(r.publications !== undefined){
				r.publications = JSON.parse(r.publications)  
			}
		}
		res.send(result[1])
	})
});

router.get('/ratemyprofessors.json', function(req, res, next) {
	con.query(ratemyprofessors_query, function(err, result){
		for(r of result[1]){
			if(r.ratingComments !== undefined && r.ratingComments !== null){
				r.ratingComments = JSON.parse(r.ratingComments)
			}
		}
		res.send(result[1])
	})
});

router.get('/googlescholar.json', function(req, res, next) {
	con.query(googlescholar_query, function(err, result){
		res.send(result)
	})
});

router.get('/', function(req, res, next){
	con.query(departments_query, function(err, result){
		res.json(result)
	})
});

module.exports = router;
