# import fs as fs
import redis
import json

data = []
# Good only if expecting strings stored...https://stackoverflow.com/questions/23256932/redis-py-and-hgetall-behavior
client = redis.StrictRedis(decode_responses=True)

print ("keys")
print(client.keys())
keys = client.keys()

for k in keys:
    # print("k",k)
    users = client.hgetall(k)
    # https://stackoverflow.com/questions/15219858/how-to-store-a-complex-object-in-redis-using-redis-py
    for u in users:
        # print("u"+k+u)
        try:
            print ("trying")
            u=json.loads(u.decode('utf-8'))
            # u = "adakjdsalkhdklas"
            print (u)
        except Exception as e:
            continue;
    data.append(users)
    print (users)
    print("\n")

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

with open('./results/data2.json', 'w') as f:
     json.dump(data, f)
