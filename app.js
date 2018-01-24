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
  , pug         = require('pug')
  , ensureTime  = true

// Database setup
redisClient = redis.createClient(rport)

redisClient.on('connect', function() {
  console.log('Connected to redis.')
})

// Data handling
var save = function save(d) {
  // console.log(pid)
  // THIS MIGHT BE IT!!!!! -> If the participant comes back at a later time then
  // when they first loaded the page...then it might get messed up or if two participants try to do something
  // at the same time
  // d.pid=pid
  redisClient.hmset(d.pid, d, function(){
  })
  // redisClient.hmset(d.postId, d)
  if( debug )
    console.log('saved to redis: ' + d.pid +', at: '+ (new Date()).toString())
}

// Server setup
var app = express()
app.use(express.bodyParser())
app.use(express.static(__dirname + '/public'))
// app.use( )
app.use('/scripts', express.static(__dirname + '/node_modules/'));
app.engine('pug', require('pug').__express)

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
  var d = req.body // Get experiment data from request body
  // If a postId doesn't exist, add one (Random number based on date)
  if (!d.postId) d.postId = (+new Date()).toString(36)
  d.timestamp = (new Date()).getTime() // Add a timestamp
  save(d) // Save the data to our database
  res.send(200) // Send a 'success' response to the frontend
})

app.post('/countBW', function handlePost(req, res){
  var d = req.body[0] // The string in the array with length=1
  var isBWCount = {"isBW": 0, "notIsBW": 0}

  redisClient.keys(d+'*', function(err, keys) { // getting the keys to loop over
    (function loop(i) {
        redisClient.hget(keys[i], 'isBW', function(err2, isBWField){ // get the isBW for the key
          if (isBWField != null){
            // console.log('isBWCount', isBWCount, keys[i], isBWField)
            if (isBWField == "true") { // redis stores boolean as a string
              // console.log('plusIsBW')
              isBWCount.isBW+=1} else {
                // console.log('plusNotISBW')
                isBWCount.notIsBW+=1}
          }
        })
        const promise = new Promise((resolve, reject) => {
            const timeout = Math.random() * 100+50; // setting random time amount before next iteration
            if (false) {reject()}
            setTimeout( () => {
                resolve(i); // resolve it!
            }, timeout);
        }).then((i)=>{
          if (i<keys.length){
            loop(i+1)
          } else {
            redisClient.hmset("isBWCount_"+d, isBWCount, ()=>{ // set the final count for the isBW
              res.send(200);
            }); }
        });
    }(0));
  })
});

app.get('/pid', function(req, res){
  // Not sure this is the right result
  return res.send('Hahahahahaha')
  // Make something for extracting
})

// app.get('/', function(req, res){
//   res.render(__dirname+"/public/indexTestJade.pug", {name: 'Al', inPID: poop})
// })

app.get('/', function(req, res){
  var loopPID = "", loopSuff = ""
  // Temporary System for checking if black and white.
  var isBWTemp = Math.floor(Math.random()*2)==1?true:false
  if (req.query.isBW!=null){
    if (req.query.isBW == 'true' || req.query.isBW == 'false'){
      isBWTemp = req.query.isBW
    }
  }
  var seed = Math.floor(Math.random()*100000) // Random seed if using number generator
  if (req.query.pid==null){ // Return error or sort of homepage index
    // res.send(404)
    res.render(__dirname+"/public/indexBasicJade.pug")
    return;
  }

  // console.log('pid', req.query.pid)
  // Create an ID based on pid
  if (req.query.pid.substring(0, 4)=="test"||req.query.pid==""){
    loopSuff = "qTest"
    let tID = req.query.pid.substring(4)
    // console.log('tID', tID, req.query.pid)
    if (tID == "") {loopPID = loopSuff+":"+(+new Date()).toString(36)} else {
      loopPID = loopSuff+":"+tID
    }
  } else if (req.query.pid.substring(0, 6) == 'iSigns'){
    loopSuff = "iSigns"
    loopPID = loopSuff+":"+req.query.pid.substring(7)
  } else {
    loopSuff = "data"
    loopPID = loopSuff+":"+req.query.pid
  }

  // Does the participant exist?
  redisClient.exists(loopPID, function (err, exist){
    if(exist){ // The participant exists
      redisClient.hget(loopPID, "graphOrder", function(err, gO){ // get graphorder
        if(gO==null){ // Rare case where participant exists but no information found, mainly encountered for testing purposes, should not for non-testing
          if (loopSuff!="qTest"||req.query.s==1){ // Session1 requested or needed if it isn't a test
            fs.writeFile('public/modules/graphOrder.json', '[{"isBW":'+isBWTemp+'}]', function(err) { // setting the graphorder to isBW so that a real graphorder can be created. If for some odd reason a participant exists but doens't have a graph order and it is not a test it is selecting isBW at random regardless of the isBWCount
              // var bwObj =[{"isBW": isBWTemp}]
              var bwObj = [{}]
              bwObj[0].isBW = isBWTemp
              res.render(__dirname+"/public/indexSess1Jade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(JSON.stringify(bwObj)) })
            })
          } else { // Make up graph order - Test Case; either session2 or testIndex
            fs.readFile('public/modules/graphOrderTest.json', 'utf8', function(err,data) {
              if (err) console.log(err);
              fs.writeFile('public/modules/graphOrder.json', data, function(err) {
                if (err) console.log(err);
                if (req.query.s==2){ // Session2 requested
                  res.render(__dirname+"/public/indexSess2Jade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(data)})
                } else { // Using test index
                  res.render(__dirname+"/public/indexTestJade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(data)})
                }
              })
            })
          }
        } else { // A graph order file exist, use
          redisClient.hmget(loopPID, "complete_s1", "complete_s2", "isBW", "time_end_s1", function(err, comp){ // Check what sessions complete
            for(var i=0; i<comp.length-1; i++){ comp[i]=comp[i]=="true"?true:false }
            console.log('caseFoosh', isBWTemp, comp)
            if (comp[2] == null || loopSuff == "qTest") {comp[2]=isBWTemp} //TODO: Check to make sure this is actually working
            if(comp[0]&&comp[1]){ // Completed
              res.render(__dirname+"/public/indexCompletedJade.pug")
            } else if (comp[0] || req.query.s==2){ //sess2
              if (ensureTime?((Date.now()-comp[3])/1000>1*7*24*60*60):true){
                // console.log('a', Date.now(), 'b', comp[3])
                res.render(__dirname+"/public/indexSess2Jade.pug", {outPID: loopPID, isBW: comp[2], outGraphOrder: JSON.stringify(gO)})
              } else {
                let timeRem = 1*7*24*60*60-(Date.now()-comp[3])/1000
                // console.log('w', timeRem, (comp[3]-Date.now())/1000)
                let days = Math.floor(parseInt(timeRem/60/60/24))
                let hr = Math.floor(parseInt(timeRem-days*60*60*24)/60/60)
                let min = Math.floor(parseInt((timeRem-hr*60*60-days*60*60*24)/60))
                res.render(__dirname+"/public/indexWait.pug", {days: days, hr: hr, min: min})
              }
            } else if (loopSuff=="qTest" && req.query.s!=1) { //test
                res.render(__dirname+"/public/indexTestJade.pug", {outPID: loopPID, isBW: comp[2], outGraphOrder: JSON.stringify(gO)})
            } else { //sess1
              res.render(__dirname+"/public/indexSess1Jade.pug", {outPID: loopPID, outSeed:0, isBW: comp[2], outGraphOrder: JSON.stringify(gO)})
            }
          })
        }
      })
    } else { // The participant doesn't exist
      // Add getting the bwCount here ... not sure I would ever have to put this above if participant exists...
      redisClient.hmget('isBWCount_'+loopSuff, "isBW", "notIsBW", function(err, comp){
        console.log('isb', comp)
        if (loopSuff !="qTest") {isBWTemp = comp[0]>comp[1]? false : true;} // decide isBWTemp based on the server
        console.log('isBWTemp', isBWTemp)
        if (loopSuff!="qTest"||req.query.s==1){ // Session1 requested or needed
          fs.writeFile('public/modules/graphOrder.json', '[{"isBW":'+isBWTemp+'}]', function(err) {
            var bwObj = [{}]
            bwObj[0].isBW = isBWTemp // For some reason need to use stringify twice
            res.render(__dirname+"/public/indexSess1Jade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(JSON.stringify(bwObj)) })
          })
        } else { // Make up graph order - Test Case; either session1 or session2
          fs.readFile('public/modules/graphOrderTest.json', 'utf8', function(err,data) {
            if (err) console.log(err);
            fs.writeFile('public/modules/graphOrder.json', data, function(err) {
              if (err) console.log(err);
              if (req.query.s==2){ // Session2 requested
                res.render(__dirname+"/public/indexSess2Jade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(data)})
              } else { // Using test index
                // console.log('test', data)
                res.render(__dirname+"/public/indexTestJade.pug", {outPID: loopPID, outSeed: seed, isBW: isBWTemp, outGraphOrder: JSON.stringify(data)})
              }
            })
          })
        }
      })
    }
  })
});

// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port)
})
