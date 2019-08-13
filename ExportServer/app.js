const http = require('http');
const mysql = require('mysql');
const fs = require('fs');
const excel = require('exceljs');
const path = require('path');

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
  database: database
});

//connect to db
con.connect(function(err){
  if(err) throw err;
  console.log('Connected!')
});

//setup sql
var data = fs.readFileSync('TableauSQLQuery.sql', 'utf8');

//setup excel worksheet
var filename = 'temp.csv';

var workbook = new excel.Workbook(); //creating workbook
var sheet = workbook.addWorksheet('Raw Values'); //creating worksheet

con.query(data, function(err, result, fields){
  if(err) console.log(err);
  sheet.addRow().values = Object.keys(result[0]);
  result.forEach(function(item, index){
    var values = [];
    values = Object.values(item);
    sheet.addRow().values = values;
    console.log(index);
  });  
  workbook.csv.writeFile(filename).then(function(){
    console.log('File created.')
  });
});

//setup rest server
var express = require("express");
var app = express();

app.use(express.static('public'));
var dir = path.join(__dirname, 'public');
app.use(express.static(dir));
app.set('view engine', 'ejs')

//start server
app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

//set homepage
app.get('/', function(req, res){
  res.render('index');
});

//set get data
app.get('/data.csv', function(req, res){
  res.sendFile(__dirname + '\\' + filename, function(err){
    if(err) console.log(err);
  });
  console.log('Sent file: ' + __dirname + '\\' + filename)
});


