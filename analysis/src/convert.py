import redis
import json
import csv
import random

# --- Begin: ALTER DUMMY DATA --- #

# import redis
# client = redis.StrictRedis(decode_responses=True)
# client.hset('qTest:Alex', 'isBW', 'true')

# --- End: ALTER DUMMY DATA --- #
# --- Begin: GLOBAL --- #

# ----- CHART TYPES AND EMBELLISHMENT TYPES
chartTypes = ['line', 'bar', 'pie']
embTypes = ['embellished', 'unrelated', 'normal']

# --- End: Global --- #
# --- Begin: CSV HEADERS --- #

# Can add an input variable to add _type to the header variables
def getHeaders():
    # Initialize and fill an array of length 6 to include all the combinations
    headers = ['p_ID', 'isBW']
    for i in chartTypes:
        for j in embTypes:
            headers.append(i+'_'+j)
    return headers


# --- End: CSV HEADERS --- #
# --- Begin: GET SESSION1 SCORE AND TIME --- #

def getSess1(inData, chartInfo, headers):
    # Headers : pID, isBW, ...variations
    # prep for CSV file
    scoreData = []
    timeData = []
    for i in range(len(inData)):
        # split PID to see if it's data I'm interested in
        dataType = inData[i]['pid'].split(':')[0]
        if dataType != 'data':
            continue
        if not inData[i]['complete_s1']:
            continue
        # Set the array by using headers to determine lengths
        scoreData.append([0]*len(headers))
        timeData.append([0]*len(headers))
        # Set participant id
        scoreData[len(scoreData)-1][0]=timeData[len(scoreData)-1][0]=inData[i]['pid']
        scoreData[len(scoreData)-1][1]=timeData[len(scoreData)-1][1]=inData[i]['graphOrder'][0]['isBW']
        # Go through the graph order and extract information
        for j in range(len(inData[i]['graphOrder'])):
            # Find embType
            embType = inData[i]['graphOrder'][j]['embType']
            for i2 in range(len(embTypes)):
                if embTypes[i2] in embType:
                    embType = embTypes[i2]
            # Find chartType
            chartType = inData[i]['graphOrder'][j]['chartType']
            for i2 in range(len(chartTypes)):
                if chartTypes[i2] in chartType:
                    chartType = chartTypes[i2]
            # Find answers for the chart
            answer = []
            for i2 in range(2):
                # Filter out the desired info by creating list of length=1 and grabbing the first(only) dictionary item
                info = [x for x in chartInfo[chartType] if x['key'] == inData[i]['graphOrder'][j]['key']][0]
                # Get the answers from the dictionary item
                answer.append(info['questionBank'][i2]['answer'])
            # Find corresponding bin
            for i2 in range(len(headers)):
                if embType in headers[i2] and chartType in headers[i2]:
                    # Get time in minutes
                    # print (data[i]['mod1'][j], '-', j)
                    time = (inData[i]['mod1'][j]['timeQEnd']-inData[i]['mod1'][j]['timeQStart'])/1000/60
                    timeData[len(scoreData)-1][i2] += time
                    # Count correct answers
                    for i3 in range(2):
                        if inData[i]['mod1'][j]['inputData'][i3]['userAnswer'] == answer[i3]:
                            scoreData[len(scoreData)-1][i2]+=1

    for i in range(len(timeData)):
        for j in range(2, len(timeData[i])):
            timeData[i][j] /= 4

    print('getSess1_score', scoreData)
    print('getSess1_time', timeData)
    return scoreData, timeData

# --- End: GET SESSION1 SCORE AND TIME  --- #
# --- Begin: GET SESSION2_mod3 SCORE AND TIME --- #
# --- Begin: GET SESSION2_mod3 SCORE AND TIME --- #

# --- Begin: WRITE DATA TO CSV --- #

def makeCSV(fileName, inData, headers, type):
    # For loop to add the type to the headers... note: or do I need? .... don't do for now XD
    with open('./results/csvFiles/'+fileName+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        if len(inData)==0:
    #        If there is nothing to write, make something up
            inData = ['madeUp', True]
            for i in range(2, len(headers)):
                inData[i].append(random.randrange(0, 100))
            inData=[1,90,100,60,10,4,80,32,77,30]
            writer.writerow(newData)
        else:
            for i in range(len(inData)):
                writer.writerow(inData[i])

# --- End: WRITE DATA TO CSV --- #
# --- Begin: MAIN --- #

def main():
    # ----- GET PARTICIPANT DATA
    data = []
    with open('./results/data2.json', 'r') as data_file:
        data = json.loads(data_file.read())

    # ----- GET ANSWER LIST
    chartInfo = []
    with open('../public/modules/graphQuestions/graphImageList.json', 'r') as data_file:
        chartInfo = json.loads(data_file.read())
    # note: perhaps make a key list to index

    headers = getHeaders()

    s1_score, s1_time = getSess1(data, chartInfo, headers)
    s1_csvNames = ['mod1_score', 'mod1_time']

    makeCSV(s1_csvNames[0], s1_score, headers, 'score')
    makeCSV(s1_csvNames[1], s1_time, headers, 'time')

    newData = []
    for i in range(100):
        # value_when_true if condition else value_when_false
        isBW = True if random.randrange(0, 2)==1 else False
        newData.append([i, isBW])
        for j in range(2, len(headers)):
            newData[i].append(random.randrange(5, 95))
    makeCSV('dummyData_time', newData, headers, 'time')

if __name__ == "__main__":
    main()

# --- End: MAIN --- #



# Make up data for variety
# newData = []
# for i in range(100):
#     newData.append([])
#     newData[i].append(i)
#     for j in range(len(headers)-1):
#         newData[i].append(random.randrange(0, 100))
