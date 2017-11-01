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
  , pid

// Database setup
redisClient = redis.createClient(rport)

redisClient.on('connect', function() {
  console.log('Connected to redis.')
})

var getBW = function getBW() {
  let isBWCount = [0, 0]
  // let keys = redisClient.keys('*')
  // let isBWArr = redisClient.mget("qTest:Alex", 'isBW')
  // console.log(isBWArr, isBWArr.length)
  redisClient.keys('*', function(err, keysO) {
    let keys = Object.keys(keysO);
    console.log('k0', keys)
    console.log('k1', keysO)
    for (let i=0; i<keys.length; i++){
      redisClient.hget(keys, "isBW", function(err, gO){
        console.log('isBW', err)
        if (err){return err} else {
          if (gO != 'null') {
            if (gO) {isBWCount[0]+=1} else {isBWCount[0]+=1}
          }
        }
      })
    }
    let pBW = isBWCount[0]>isBWCount[1]?false:true
    console.log('returning', pBW, isBWCount)
    return (pBW)
  })
}

// Data handling
var save = function save(d) {
  // console.log(pid)
  d.pid=pid
  redisClient.hmset(pid, d)
  // redisClient.hmset(d.postId, d)
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
// Alyssa Note: This isn't called anywhere.
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
  // Get experiment data from request body
  var d = req.body
  // If a postId doesn't exist, add one (Random number based on date)
  if (!d.postId) d.postId = (+new Date()).toString(36)
  // Add a timestamp
  d.timestamp = (new Date()).getTime()
  // Save the data to our database
  save(d)
  // Send a 'success' response to the frontend
  res.send(200)
})

app.get('/', function(req, res){
  // getBW()
  function checkColor(){
    return Math.floor(Math.random()*2)==1?true:false
  }
  // Query the string, if null -> error, test -> make stuff up, pid -> check if first time
  if (req.query.pid==null){
    // Link is invalid
    res.send(404)
    return;
  } else if (req.query.pid=="test"){
    pid = "qTest:"+(req.query.name!=null?req.query.name:(+new Date()).toString(36))
    // If first session asked for -> use session one index
    if (req.query.s==1){
      fs.writeFile('public/modules/graphOrder.json', '['+checkColor().toString()+']', function(err) {
        res.sendfile(__dirname+"/public/indexSess1.html")
      })
    } else {
      // Copying a dummy chart order JSON into the chart order JSON read client side.
      fs.readFile('public/modules/graphOrderTest.json', 'utf8', function(err,data) {
        if (err) console.log(err);
        fs.writeFile('public/modules/graphOrder.json', data, function(err) {
          if(err) console.log(err);
          // Sending corresponding index file.
          if (req.query.s == 2){
            res.sendfile(__dirname+"/public/indexSess2.html")
          } else {
            res.sendfile(__dirname+"/public/indexTest.html")
          }
        });
      })
    }
  } else {
    // If the first four characters in string are data then it will be used for testing
    if (req.query.pid.substring(0, 6) == 'iSigns'){
      let parID = (+new Date()).toString(36)
      if (req.query.pid.substring(7)!=''){parID = req.query.pid.substring(7)}
      pid = "p:"+parID
    } else {
      pid = "data:"+req.query.pid
    }
    // Do something if exist
    function direct(suff){
      // Grab the chart order from the database and copy into JSON that will be read client side
      redisClient.hget(suff+":"+req.query.pid, "graphOrder", function(err, gO){
        // Could also use a template like jade or something to inject into html or make things dynamic using socket.io.
        if (gO==null){
          // Somehow the chart order was not in database, redirecting to session one.
          // console.log("graphOrderDNE")
          fs.writeFile('public/modules/graphOrder.json', '['+checkColor().toString()+']', function(err) {
            res.sendfile(__dirname+"/public/indexSess1.html")
          })
          return;
        }
        fs.writeFile('public/modules/graphOrder.json', gO, function(err) {
          if(err) console.log(err);
          res.sendfile(__dirname+"/public/indexSess2.html")
        });
      })
    }
    // Lookup if user in database, ex: pid = p:j60wtjs8
    redisClient.exists("p:"+req.query.pid, function (err, exist){
      // If the participant exists pull up session 2.
      if (exist){
        direct('p')
      } else {
        // The entry doesn't exist. Pull up session 1
        redisClient.exists("data:"+req.query.pid, function (err, exist){
          if (exist){direct('data')} else{
            fs.writeFile('public/modules/graphOrder.json', '['+checkColor().toString()+']', function(err) {
              res.sendfile(__dirname+"/public/indexSess1.html")
            })
          }
        })
      }
    })
  }
});

// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port)
})
