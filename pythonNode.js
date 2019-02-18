var cors = require('cors');
var csvParser = require('csv-parse');
var fs = require("fs");
var express = require('express');
var mysql = require('mysql');
const bodyParser = require("body-parser");
var app = express();
app.use(cors());

var globals = {};

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "123456789",
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
  
  
  app.post("/argsPython", function(req, res) {
     globals.keyword = req.body.question;
      console.log("Keyword is", globals.keyword);
    });


app.post("/file", function(req, res) {
  let uploadFile = req.files;
  // const fileName = req.files[0].name;
  // console.log(uploadFile);
 console.log(uploadFile);
  
});
 

    app.get('/pythonscript', (req, res) => {
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
});


