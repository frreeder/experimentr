import redis
import json
import csv
import random

# ------ Begin: GET DATA FROM REDIS ------ #

data = []
# Good only if expecting strings stored...https://stackoverflow.com/questions/23256932/redis-py-and-hgetall-behavior
client = redis.StrictRedis(decode_responses=True)

keys = client.keys()
print(keys)

for k in keys:
    # print("k",k)
    if 'isBWCount' in k: # do not count the counters for isBW
        continue;
    users = client.hgetall(k)
    # https://stackoverflow.com/questions/15219858/how-to-store-a-complex-object-in-redis-using-redis-py
    for u in users:
        try:
            users[u]=json.loads(users[u])
            continue;
        except ValueError as e:
            continue;
    data.append(users)

with open('./results/data2.json', 'w') as f:
     json.dump(data, f, indent=4) #indent makes JSON easier to read

# ------ End: GET DATA FROM REDIS ------ #













# ------- Because Alyssa is too dumb to delete. ------ #
# client.on('connect', keys)

# def keys:
#   client.keys("*", *):
#
#   function (err, res) {
#     console.log(res)
#     res.forEach(data)
#     client.quit()
#   });
#
# function data (k, i, arr) {
#   client.hgetall(k, function (err, obj) {
#     // This is a gross way of checking for all string JSON objects and parsing if true.
#     for (var j in obj) {
#       try {
#         obj[j]=JSON.parse(obj[j]);
#       } catch (e){
#       }
#     }
#     dataset.push(obj)
#     if(i === arr.length-1) log(dataset)
#   });
# }
#
# function log (obj) {
#   console.log(JSON.stringify(obj))
# }
