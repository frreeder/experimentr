/* global require:true, console:true, process:true, __dirname:true */
'use strict'

// Example run command: `node app.js 9000 6380 true`; listen on port 9000, connect to redis on 6380, debug printing on.

var express     = require('express')
  , http        = require('http')
  , redis       = require('redis')
  , redisClient
  , port        = process.argv[2] || 3000
  , rport       = process.argv[3] || 6379
  , debug       = process.argv[4] || null
  , path        = require('path')
  , fs          = require('fs')

// Database setup
redisClient = redis.createClient(rport)

redisClient.on('connect', function() {
  console.log('Connected to redis.')
})

// Data handling
var save = function save(d) {
  redisClient.hmset(d.postId, d)
  if( debug )
    console.log('saved to redis: ' + d.postId +', at: '+ (new Date()).toString())
}

// Server setup
var app = express()
app.use(express.bodyParser())
app.use(express.static(__dirname + '/public'))
// app.use( )
app.use('/scripts', express.static(__dirname + '/node_modules/'));

// If the study has finished, write the data to file
// This isn't called anywhere...
app.post('/finish', function(req, res) {
  // console.log("finished!!!")
  fs.readFile('public/modules/blocked-workers.json', 'utf8', function(err,data) {
    if (err) console.log(err);
    var data = JSON.parse(data);
    data.push(req.body.workerId);
    data = JSON.stringify(data);
    fs.writeFile('public/modules/blocked-workers.json', data, function(err) {
      if(err) console.log(err);
    });
  });

  res.send(200)
})

// Handle POSTs from frontend
app.post('/', function handlePost(req, res) {
  // console.log("posting")
  // Get experiment data from request body
  var d = req.body
  // If a postId doesn't exist, add one (it's random, based on date)
  if (!d.postId) d.postId = (+new Date()).toString(36)
  // Add a timestamp
  d.timestamp = (new Date()).getTime()
  // Save the data to our database
  save(d)
  // Send a 'success' response to the frontend
  res.send(200)
})

app.get('/', function(req, res){
  // Query the string, takes the pid to identify participant and only uses version if testing
  // ?pid=j4bn8lpy&v=1
  // console.log("q: " + req.query.pid + " s: " + req.query.s)
  if (req.query.pid==null){
    // telling participant link is invalid, not sure if I want to do other stuff here
    res.send(404)
    return;
  } else if (req.query.pid=="test"){
    // checks to see if session specified, if not using a default index file
    if (req.query.s==1){
      res.sendfile(__dirname+"/public/indexSess1.html")
    } else {
      // so gross but will read contents of test and paste into graph order
      fs.readFile('public/modules/graphOrderTest.json', 'utf8', function(err,data) {
        if (err) console.log(err);
        fs.writeFile('public/modules/graphOrder.json', data, function(err) {
          if(err) console.log(err);
          // if session 2 or default index file
          if (req.query.s == 2){
            res.sendfile(__dirname+"/public/indexTest.html")
          } else {
            res.sendfile(__dirname+"/public/indexSess2.html")
          }
        });
      })
    }
  } else {
    // Lookup if user in database, ex: pid = j60wtjs8
    redisClient.exists(req.query.pid, function (err, exist){
      // If the participant exists pull up session 2.
      if (exist){
        // graph order is added in session and is the randomization of the graphs
        redisClient.hget(req.query.pid, "graphOrder", function(err, gO){
          // Adding the graph order to a json file to be accessed on client side
          // Could also use a template like jade or something to inject into html
          // or make things dynamic using socket.io ...
          fs.writeFile('public/modules/graphOrder.json', gO, function(err) {
            if(err) console.log(err);
            res.sendfile(__dirname+"/public/indexSess2.html")
          });
        })
      } else {
        // The entry doesn't exist. Pull up session 1
        res.sendfile(__dirname+"/public/indexSess1.html")
      }
    })
  }




  // res.sendFile(path.join(__dirname + '/public/indexw.html'))
  // console.log(__dirname+"/public/indexw.html")
  // res.send('apple: ' + "pot");
  // redisClient
  // fs.writeFile('public/modules/graphOrder.json', 'utf8', function(err,data) {
  //
  // // }, res.sendfile(__dirname+"/public/indexw.html"))
  // res.sendfile(__dirname+"/public/indexw.html")
  // console.log(req.query.id)
  // res.write({apple: "pot"})
});

// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port)
})
