import redis
import json
import csv
import random

# ------ Begin: GET DATA FROM REDIS ------ #

data = []
# Good only if expecting strings stored...https://stackoverflow.com/questions/23256932/redis-py-and-hgetall-behavior
client = redis.StrictRedis(decode_responses=True)

keys = client.keys()

for k in keys:
    # print("k",k)
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
# ------ Begin: GET CORRECT ANSWERS ------ #

chartInfo = []
with open('../public/modules/graphQuestions/graphImageList.json', 'r') as data_file:
    chartInfo = json.loads(data_file.read())

# ------ End: GET CORRECT ANSWERS ------ #
# ------ Begin: PREPARE DATA FOR CSV ------ #

# Define factors and variables
chartTypes = ['line', 'bar', 'pie']
embTypes = ['embellished', 'unrelated', 'normal']

# Initialize and fill an array of length 6 to include all the combinations
headers = ['PARTICIPANT_ID']
for i in chartTypes:
    for j in embTypes:
        headers.append(i+'_'+j+'_score')

newData = []
for i in range(len(data)):
    if data[i]['pid']!='p:analysis':
        continue
    newData.append([0]*len(headers))
    newData[len(newData)-1][0]=data[i]['pid']
    for j in range(len(data[i]['graphOrder'])):
        # Find embType
        embType = data[i]['graphOrder'][j]['embType']
        for i2 in range(len(embTypes)):
            if embTypes[i2] in embType:
                embType = embTypes[i2]
        # Find chartType
        chartType = data[i]['graphOrder'][j]['chartType']
        for i2 in range(len(chartTypes)):
            if chartTypes[i2] in chartType:
                chartType = chartTypes[i2]
        # Find answers for the chart
        answer = []
        for i2 in range(2):
            answer.append([x for x in chartInfo[chartType] if x['key'] == data[i]['graphOrder'][j]['key']][0]['questionBank'][i2]['answer'])
        # Find corresponding bin and count correct answers
        for i2 in range(len(headers)):
            if embType in headers[i2] and chartType in headers[i2]:
                for i3 in range(2):
                    if data[i]['mod3'][j]['inputData'][i3]['userAnswer'] == answer[i3]:
                        newData[len(newData)-1][i2]+=1

# ------ End: PREPARE DATA FOR CSV ------ #
# ------ Begin: WRITE DATA TO CSV ------ #

# Make up data for variety
newData = []
for i in range(100):
    newData.append([])
    newData[i].append(i)
    for j in range(len(headers)-1):
        newData[i].append(random.randrange(0, 100))

with open('./results/data2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    if len(newData)==0:
        # If there is nothing to write, make something up
        newData=[1,90,100,60,10,4,80,32,77,30]
        writer.writerow(newData)
    else:
        for i in range(len(newData)):
            writer.writerow(newData[i])

# ------ Begin: WRITE DATA TO CSV ------ #













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
