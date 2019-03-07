var cors = require('cors');
var csvParser = require('csv-parse');
const csv = require('csv-parser')
var fs = require("fs");
var express = require('express');
var mysql = require('mysql');
const bodyParser = require("body-parser");
var fileupload = require("express-fileupload");

var app = express();
app.use(cors());

var globals = {};

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password",
    database: "test"
  });

app.listen(3001, function() {
    console.log('server running on port 3001');
} )

app.use(
    bodyParser.urlencoded({
      extended: true
    })
  );
  
  app.use(bodyParser.json());
  app.get('/mysql', (req, res) => {
    con.connect(function(err) {
    
      con.query("SELECT Tweets FROM twitter ORDER BY RTs DESC LIMIT 3", function (err, result, fields) {
        if (err) throw err;
        console.log(result);
        res.send(result);
      });
    });
  });
  app.get('/areachart', (req, res) => {
    con.connect(function(err) {
      
      con.query("SELECT Name, RTs, Likes, SA FROM twitter ORDER BY RTs DESC LIMIT 10", function (err, result, fields) {
        if (err) throw err;
        console.log(result);
        res.send(result);
      });
    });
  });

  app.get('/globalchart', (req, res) => {
    con.connect(function(err) {
      
      con.query("SELECT Location, RTs, SA FROM twitter ORDER BY RTs DESC LIMIT 10", function (err, result, fields) {
        if (err) throw err;
        console.log(result);
        res.send(result);
      });
    });
  });
  
  
  app.post("/argsPython", function(req, res) {
    if(req.body.question != null){
      globals.keycount = true;
    }
     globals.keyword = req.body.question;
      console.log("Keyword is", globals.keyword);
    });

    app.use(fileupload())   ;
app.post("/file", function(req, res) {
  var file;

if(!req.files)
    {
        res.send("File was not found");
        globals.filecount =false;
        return;
    }
    globals.filecount =true;
    globals.csvfile = req.files;
console.log(req.files.file.name);
    res.send("File Uploaded");
      csvParser(req.files.file.data, {
    delimiter: ',',
    ltrim: true, 
    rtrim: true,
  }, function(err, data) {
    if (err) {
      console.log(err);
    } else {
      console.log(data);
      globals.fetchdata = data;
      // var obj = globals.fetchdata;
      // console.log('data', globals.fetchdata);
      for (let item of globals.fetchdata){
        console.log(item);
      }
    }
  });
});
 

    app.get('/pythonscript', (req, res) => {
      if ( globals.keycount == true)
      {
        var obj = globals.keyword;
        console.log(obj); 
    var spawn = require("child_process").spawn;
    var process = spawn('python2.7',["./pythoncode.py", obj] );
    process.stdout.on('data', function(data) {
        res.send(data.toString());
    } )
    process.stderr.on("data", function(data) {
      console.log('stderr: ' + data);
  } )
      }
       else if (globals.fetchdata != null){
        for (let item of globals.fetchdata){
          console.log(item);
    var spawn = require("child_process").spawn;
    var process = spawn('python2.7',["./pythoncode.py", item] );
//     process.stdout.on('data', function(data) {
//       res.send(data.toString());
//   } )
//   process.stderr.on("data", function(data) {
//     console.log('stderr: ' + data);
// } )
  }
    process.stdout.on('data', function(data) {
        res.send(data.toString());
    } )
    process.stderr.on("data", function(data) {
      console.log('stderr: ' + data);
  } )
       }
       else {
         console.log('No Item is entered');
       }
});


