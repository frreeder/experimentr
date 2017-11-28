import redis
import json
import csv
import random
import numpy as np

# --- Begin: ALTER DUMMY DATA --- #

# import redis
# client = redis.StrictRedis(decode_responses=True)
# client.hset('qTest:Alex', 'isBW', 'true')

# --- End: ALTER DUMMY DATA --- #
# --- Begin: GLOBAL --- #

# ----- CHART TYPES AND EMBELLISHMENT TYPES
chartTypes = ['line', 'bar', 'pie']
embTypes = ['embellished', 'unrelated', 'normal']

# Based on what I know about the data.
embTDict = {'embellished':0, 'unrelated':1, 'unrelated2':1, 'normal':2, 'normal2':2}

def getInfo():
    with open('../public/modules/graphQuestions/graphImageList.json', 'r') as data_file:
        chartInfo = json.loads(data_file.read())
    cIDict = {}
    cTDict = {}
    for gType in chartInfo:
        for i in range(len(chartInfo[gType])):
            cIDict[chartInfo[gType][i]['key']] = i
            cTDict[chartInfo[gType][i]['title']] = chartInfo[gType][i]['key']
    print(cIDict)
    return cIDict, cTDict

chartKeyDict, chartTitleDict = getInfo()

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

def getMod_1_3(inData, chartInfo, headers, inModName):
    scoreData = []
    timeData = []
    for i in range(len(inData)):
        print('\n g13', inData[i]['pid'])
        # split PID to see if it's data I'm interested in
        dataType = inData[i]['pid'].split(':')[0]
        if dataType != 'data':
            continue
        if not inData[i]['complete_s1'] and inModName == 'mod1':
            continue
        if not inData[i]['complete_s2'] and inModName == 'mod3':
            continue
        # Set the array by using headers to determine lengths
        scoreData.append([0]*len(headers))
        timeData.append([0]*len(headers))
        # Set pid and isBW
        scoreData[len(scoreData)-1][0]=timeData[len(scoreData)-1][0]=inData[i]['pid']
        scoreData[len(scoreData)-1][1]=timeData[len(scoreData)-1][1]=inData[i]['graphOrder'][0]['isBW']
        # Go through the graph order and extract information
        for j in range(len(inData[i]['graphOrder'])):
            # Get embType and chartType
            embType = embTypes[embTDict[inData[i]['graphOrder'][j]['embType']]]
            chartType = inData[i]['graphOrder'][j]['chartType']
            # Find answers for the chart
            answer = []
            for i2 in range(2):
                # Use dictionary to get the desired chart information
                info = chartInfo[chartType][chartKeyDict[inData[i]['graphOrder'][j]['key']]]
                # Append answer to the chart
                answer.append(info['questionBank'][i2]['answer'])
            # Find corresponding bin by finding the index using chart and emb type
            hI = headers.index(chartType+'_'+embType)
            # Get time in minutes
            # Time in seconds, divide by 60 to get minutes.
            time = (inData[i][inModName][j]['timeQEnd']-inData[i][inModName][j]['timeQStart'])/1000
            timeData[len(scoreData)-1][hI] += time
            # Count correct answers
            for i3 in range(2):
                if inData[i][inModName][j]['inputData'][i3]['userAnswer'] == answer[i3]:
                    scoreData[len(scoreData)-1][hI]+=1
        print('done')

    for i in range(len(timeData)):
        for j in range(2, len(timeData[i])):
            timeData[i][j] /= 2

    print('getMod_1_3_score', scoreData)
    print('getMod_1_3_time', timeData)
    return scoreData, timeData

# --- End: GET SESSION1 SCORE AND TIME  --- #
# --- Begin: GET SESSION2_mod2 SCORE AND TIME --- #

def getMod_2(inData, chartInfo, headers):
    inModName = 'mod2'
    scoreData = []
    timeData = []
    for i in range(len(inData)):
        # split PID to see if it's data I'm interested in -> THESE SHOULD BE OUTSIDE... maybe?
        dataType = inData[i]['pid'].split(':')[0]
        if dataType != 'data':
            continue
        if not inData[i]['complete_s2']:
            continue
        # Set the array by using headers to determine lengths
        scoreData.append([0]*len(headers))
        timeData.append([0]*len(headers))
        # Set pid and isBW
        scoreData[len(scoreData)-1][0]=timeData[len(scoreData)-1][0]=inData[i]['pid']
        scoreData[len(scoreData)-1][1]=timeData[len(scoreData)-1][1]=inData[i]['graphOrder'][0]['isBW']

        # For mod2; get the titles
        titleList = list(chartTitleDict.keys())

        # Get the titles answered
        titleAns = []
        accList = inData[i][inModName]
        # acc = 'userInput' # temporary
        acc = 'inputData'  # ----> modify application to save like this
        for page in accList:
            for i3 in range(len(page[acc])):
                # print(page[acc][i3]['userAnswer']) #problem -> saved title...not the key a)fix it over there b)fix it here
                if page[acc][i3]['userAnswer'] in titleList:
                    titleAns.append(chartTitleDict[page[acc][i3]['userAnswer']])
        # print ('titleAns', titleAns)

        # Go through the graph order to help understand what bin to put the information
        for j in range(len(inData[i]['graphOrder'])):
            # Get embType and chartType
            embType = embTypes[embTDict[inData[i]['graphOrder'][j]['embType']]]
            chartType = inData[i]['graphOrder'][j]['chartType']
            chartKey = inData[i]['graphOrder'][j]['key']
            # Find corresponding bin by finding the index using chart and emb type
            hI = headers.index(chartType+'_'+embType)
            # Get time in minutes
            # Time in seconds, divide by 60 to get minutes.
            time = (inData[i][inModName][len(inData[i][inModName])-1]['timeQEnd']-inData[i][inModName][0]['timeQStart'])/1000
            timeData[len(scoreData)-1][hI] += time
            # Check if answers are correct.
            # correct, incorrect
            if chartKey in titleAns:
                scoreData[len(scoreData)-1][hI] += 1

    for i in range(len(timeData)):
        for j in range(2, len(timeData[i])):
            timeData[i][j] /= 2

    print('getMod_2_score', scoreData)
    print('getMod_2_time', timeData)
    return scoreData, timeData

# --- End: GET SESSION2_mod2 SCORE AND TIME --- #
# --- Begin: GET SESSION2_mod4 SCORE AND TIME --- #

def getMod_4(inData, chartInfo, headers):
    inModName = 'mod4'
    scoreData = []
    timeData = []
    selDict = {'bar': 'selBar', 'pie': 'pointLoc', 'line': 'pointLoc'}
    for i in range(len(inData)):
        # split PID to see if it's data I'm interested in
        dataType = inData[i]['pid'].split(':')[0]
        if dataType != 'data':
            continue
        if not inData[i]['complete_s2']:
            continue
        # Set the array by using headers to determine lengths
        scoreData.append([0]*len(headers))
        timeData.append([0]*len(headers))
        # Set pid and isBW
        scoreData[len(scoreData)-1][0]=timeData[len(scoreData)-1][0]=inData[i]['pid']
        scoreData[len(scoreData)-1][1]=timeData[len(scoreData)-1][1]=inData[i]['graphOrder'][0]['isBW']
        # Go through the graph order and extract information
        for j in range(len(inData[i]['graphOrder'])):
            # Get embType and chartType
            embType = embTypes[embTDict[inData[i]['graphOrder'][j]['embType']]]
            chartType = inData[i]['graphOrder'][j]['chartType']

            # Find corresponding bin by finding the index using chart and emb type
            hI = headers.index(chartType+'_'+embType)

            # Get time in minutes
            # Time in seconds, divide by 60 to get minutes.
            time = (inData[i][inModName][j]['timeQEnd']-inData[i][inModName][j]['timeQStart'])/1000
            timeData[len(scoreData)-1][hI] += time

            # Use dictionary to get the desired chart information
            info = chartInfo[chartType][chartKeyDict[inData[i]['graphOrder'][j]['key']]]

            # Get the index of the chart value being manipulated
            cInd  = info['interact'][selDict[chartType]]

            # Read the csv file and get the manipulated chart value and max value
            cVal = 0
            cMax = 0
            with open('../public/'+info['interact']['dataPath'], 'r') as csvfile:
                reader = csv.reader(csvfile)
                csvI = 0
                for row in reader:
                    if csvI!=0:
                        if chartType == 'pie':
                            cMax += float(row[1])
                        elif csvI == 1 or cMax < float(row[1]):
                            cMax = float(row[1])
                        if csvI == cInd + 1:
                            cVal = float(row[1])
                    csvI += 1
            # print ('\n', info['title'])
            # print ('cVal, cMax: ', cVal, cMax)

            # Grab the user answer (value)
            uVal = inData[i][inModName][j]['inputData'][0]['userAnswer']
            # print ('uVal', uVal)

            diff = abs(cVal - uVal)
            scoreData[len(scoreData)-1][hI] += (cMax - diff)/cMax
            # print('diff', diff, ', score', (cMax - diff)/cMax)

    for i in range(len(timeData)):
        for j in range(2, len(timeData[i])):
            # print ('s', scoreData[i][j])
            scoreData[i][j] /= 2
            timeData[i][j] /= 2

    print('getMod_4_score', scoreData)
    print('getMod_4_time', timeData)
    return scoreData, timeData

# --- End: GET SESSION2_mod4 SCORE AND TIME --- #
# --- Begin: GET SESSION2_mod5 SCORE AND TIME --- #

def getMod_5(inData, chartInfo, headers):
    inModName = 'mod5'
    scoreData = []
    timeData = []
    for i in range(len(inData)):
        # split PID to see if it's data I'm interested in
        dataType = inData[i]['pid'].split(':')[0]
        if dataType != 'data':
            continue
        if not inData[i]['complete_s2']:
            continue
        # Set the array by using headers to determine lengths
        scoreData.append([0]*len(headers))
        timeData.append([0]*len(headers))
        # Set pid and isBW
        scoreData[len(scoreData)-1][0]=timeData[len(scoreData)-1][0]=inData[i]['pid']
        scoreData[len(scoreData)-1][1]=timeData[len(scoreData)-1][1]=inData[i]['graphOrder'][0]['isBW']
        # Go through the graph order and extract information
        for j in range(len(inData[i]['graphOrder'])):
            # Get embType and chartType
            embType = embTypes[embTDict[inData[i]['graphOrder'][j]['embType']]]
            chartType = inData[i]['graphOrder'][j]['chartType']

            # Use dictionary to get the desired chart information
            info = chartInfo[chartType][chartKeyDict[inData[i]['graphOrder'][j]['key']]]

            # Find corresponding bin by finding the index using chart and emb type
            hI = headers.index(chartType+'_'+embType)

            # Time in seconds, divide by 60 to get minutes.
            time = (inData[i][inModName][j]['timeQEnd']-inData[i][inModName][j]['timeQStart'])/1000
            timeData[len(scoreData)-1][hI] += time

            # Find answers for the chart and see if correct
            for qI in range(len(info['themeQuestions'])):
                answer = info['themeQuestions'][qI]['answer']
                # print ('an', answer, inData[i][inModName][j]['inputData'][qI]['userAnswer'])
                if inData[i][inModName][j]['inputData'][qI]['userAnswer'] == answer:
                    scoreData[len(scoreData)-1][hI]+=1

    for i in range(len(timeData)):
        for j in range(2, len(timeData[i])):
            timeData[i][j] /= 2

    print('getMod_5_score', scoreData)
    print('getMod_5_time', timeData)
    return scoreData, timeData

# --- End: GET SESSION2_mod5 SCORE AND TIME --- #
# --- Begin: WRITE DATA TO CSV --- #

def makeCSV(filePath, fileName, inData, headers, type):
    # For loop to add the type to the headers... note: or do I need? .... don't do for now XD
    with open(filePath+fileName+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        if len(inData)!=0:
            for i in range(len(inData)):
                writer.writerow(inData[i])

# --- End: WRITE DATA TO CSV --- #
# --- Begin: MAIN --- #

def main():
    # ----- GET PARTICIPANT DATA
    data = []
    # filePath = './results/data2.json'
    filePath = './vmResults/JSONData/data2.json'

    # csvFilePath = './results/csvFiles/'
    csvFilePath = './vmResults/csvFiles/'

    with open(filePath, 'r') as data_file:
        data = json.loads(data_file.read())

    # ----- GET ANSWER LIST
    # getInfo(data) # problem with this is that I don't want a really long chart info.... ugh
    chartInfo = []
    with open('../public/modules/graphQuestions/graphInfo.json', 'r') as data_file:
        chartInfo = json.loads(data_file.read())
    # note: I want to return different things; ex: answers, original csv information.
    # note: I want to make a index for easily finding what I want....

    headers = getHeaders()

    s1_m1_score, s1_m1_time = getMod_1_3(data, chartInfo, headers, 'mod1')
    csvNames = ['mod1_score', 'mod1_time']

    if len(s1_m1_score) != 0:
        makeCSV(csvFilePath, csvNames[0], s1_m1_score, headers, 'score')
        makeCSV(csvFilePath, csvNames[1], s1_m1_time, headers, 'time')

    s2_m3_score, s2_m3_time = getMod_1_3(data, chartInfo, headers, 'mod3')
    csvNames = ['mod3_score', 'mod3_time']

    if len(s2_m3_score) != 0:
        makeCSV(csvFilePath, csvNames[0], s2_m3_score, headers, 'score')
        makeCSV(csvFilePath, csvNames[1], s2_m3_time, headers, 'time')

    # I'm thinking of adding a csv file with a more detailed view of the charts... I don't know.
    s2_m2_score, s2_m2_time = getMod_2(data, chartInfo, headers)
    csvNames = ['mod2_score', 'mod2_time']

    if len(s2_m2_score) != 0:
        makeCSV(csvFilePath, csvNames[0], s2_m2_score, headers, 'score')
        # For the second module, there is really only one time....I think.
        newHeaders = headers[:2]
        newHeaders.append('time')
        makeCSV(csvFilePath, csvNames[1], np.array(s2_m2_time)[:, :3], newHeaders, 'time')

    # Not saving values properly for line and pie...maybe bar? I dunno
    s2_m4_score, s2_m4_time = getMod_4(data, chartInfo, headers)
    csvNames = ['mod4_score', 'mod4_time']

    if len(s2_m4_score) != 0:
        makeCSV(csvFilePath, csvNames[0], s2_m4_score, headers, 'score')
        makeCSV(csvFilePath, csvNames[1], s2_m4_time, headers, 'time')

    # s2_m5_score, s2_m5_time = getMod_5(data, chartInfo, headers)
    # csvNames = ['mod5_score', 'mod5_time']
    #
    # if len(s2_m5_score) != 0:
    #     makeCSV(csvFilePath, csvNames[0], s2_m5_score, headers, 'score')
    #     makeCSV(csvFilePath, csvNames[1], s2_m5_time, headers, 'time')

    # Making a dummy file for analyis
    newData = []
    for i in range(100):
        # value_when_true if condition else value_when_false
        isBW = True if random.randrange(0, 2)==1 else False
        newData.append([i, isBW])
        for j in range(2, len(headers)):
            newData[i].append(random.randrange(5, 95))
    makeCSV(csvFilePath, 'dummyData_time', newData, headers, 'time')

if __name__ == "__main__":
    main()

# --- End: MAIN --- #
