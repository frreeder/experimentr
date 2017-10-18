import os
import json
from pprint import pprint
import cv2

with open('interactUnrelated.json') as data_file:
    data = json.load(data_file)
    print("d", data)

graphTypes = ("line", "pie", "bar")

fileNames = os.listdir("./graphImages/interact")
fileNamesBW = os.listdir("./graphImages/interact_bw")

# LINE
inList=("interact_00", "interact_01", "interact_02")
for x in fileNames:
    if "line" in x:
        for i in data["line"]:
            for j in data["line"][i]:
                # print("j", j)
                    if j["key"] in x:
                        for ind, k in enumerate(inList):
                            if k in x:
                                print ("iCaught: ", x)
                                if ind == 0:
                                    img = cv2.imread("./graphImages/interact/"+x,1)
                                    j["imageDim"]= (img.shape[1], img.shape[0])
                                if ind == 2:
                                    img = cv2.imread("./graphImages/interact/"+x,1)
                                    j["iconDim"]=(img.shape[1], img.shape[0])
                                j["imagePath"].append("modules/graphQuestions/graphImages/interact/"+x)

inList=("interact_bw_00", "interact_bw_01", "interact_bw_02")
for x in fileNamesBW:
    if "line" in x:
        for i in data["line"]:
            for j in data["line"][i]:
                    if j["key"] in x:
                        for ind, k in enumerate(inList):
                            if k in x:
                                j["imagePathBW"].append("modules/graphQuestions/graphImages/interact_bw/"+x)


# pie
for i in data["pie"]:
    for j in data["pie"][i]:
        # print("j", j)
        for ind, k in enumerate(j["imgPath"]):
            for x in fileNames:
                if "pie" in x and j["key"] in x and k in x:
                    print ("iCaught: ", x)
                    # might not need iconDim
                    img = cv2.imread("./graphImages/interact/"+x,1)
                    j["imagePath"].append({"path": "modules/graphQuestions/graphImages/interact/"+x, "iconDim": (img.shape[1], img.shape[0])})

for i in data["pie"]:
    for j in data["pie"][i]:
        for ind, k in enumerate(j["imgPathBW"]):
            for x in fileNamesBW:
                if "pie" in x and j["key"] in x and k in x:
                    img = cv2.imread("./graphImages/interact_bw/"+x,1)
                    j["imagePathBW"].append({"path": "modules/graphQuestions/graphImages/interact_bw/"+x, "iconDim": (img.shape[1], img.shape[0])})

for j in data["pie"]:
    print ("j", j)
    for k in data["pie"][j]:
        print ("k", k)
        del k["imgPath"]
        del k["imgPathBW"]

# bar
for i in data["bar"]:
    for j in data["bar"][i]:
        for ind, k in enumerate(j["imgPath"]):
            for x in fileNames:
                if j["key"] in x and "bar" in x and k in x:
                    print ("iCaught: ", x)
                    if ind == 0:
                        img = cv2.imread("./graphImages/interact/"+x,1)
                        j["imageDim"]= (img.shape[1], img.shape[0])
                    if ind == 1:
                        img = cv2.imread("./graphImages/interact/"+x,1)
                        j["barDim"]= (img.shape[1], img.shape[0])
                    j["imagePath"].append("modules/graphQuestions/graphImages/interact/"+x)
                    continue

for i in data["bar"]:
    for j in data["bar"][i]:
        for ind, k in enumerate(j["imgPathBW"]):
            for x in fileNamesBW:
                if j["key"] in x and "bar" in x and k in x:
                    j["imagePathBW"].append("modules/graphQuestions/graphImages/interact_bw/"+x)
                    continue

for j in data["bar"]:
    print ("j", j)
    for k in data["bar"][j]:
        print ("k", k)
        del k["imgPath"]
        del k["imgPathBW"]

with open('interactData.json', 'w') as f:
     json.dump(data, f, indent=4)
