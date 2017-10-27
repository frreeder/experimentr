import os
import json
from pprint import pprint
import cv2

# I can open the json file
# Using with opens and closes the file. See: http://effbot.org/zone/python-with-statement.htm
with open('graphImageList.json') as data_file:
    data = json.load(data_file)

graphTypes = ("line", "pie", "bar")

for i in data:
    print ("i", i)
    for j in data[i]:
        # https://stackoverflow.com/questions/521674/initializing-a-list-to-a-known-number-of-elements-in-python
        j["imagePath"]=["modules/graphQuestions/graphImages/final_color/rangerPoseGreen.png"] * 5
        pprint(j)
        print(j["title"])

# Adding data path and other to line
for j in data["line"]:
    j["interact"]["imagePath"]=["modules/graphQuestions/graphImages/final_color/rangerPoseGreen.png"] * 2
    j["interact"]["withIcon"]= False
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/line_data_"+j["key"]+".csv"

# Adding an data path and other to pie
for j in data["pie"]:
    j["interact"]["withIcon"]= False
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/pie_data_"+j["key"]+".csv"

# Adding data path to bar
for j in data["bar"]:
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/bar_data_"+j["key"]+".csv"

# for all the images!
allImages = []

pprint(data["line"][0])

# fileNames = filter(lambda x: x.endswith('.txt'), os.listdir('mydir'))
fileNames = os.listdir("./graphImages/final_color")
fileNamesBW = os.listdir("./graphImages/final_bw")

interactNames = os.listdir("./graphImages/interact")
interactBWNames = os.listdir("./graphImages/interact_bw")

baseNames = os.listdir("../graphTheme/chartBase")

# A method using endswith to fileter out the png
# txt_files = list(filter(lambda x: x.endswith('.png'), os.listdir('.')))
# print("using endswith and .png", txt_files)

# Showing what happens if path doesnot have a name.
# stuff = os.path.splitext(".json")
# print (stuff)

txt_files2 = list(filter(lambda x: os.path.splitext(x)[1]==".png", os.listdir('.')))
print("using splittext and .json", txt_files2)

# Not super familiar with this but it seems like a condensed for in loop with a if statement
# Why use x twice? http://www.pythonforbeginners.com/basics/list-comprehensions-in-python
# something = ( x for x in fileNames if x.endswith('.png') )
# print ("using for in and if and .json", list(something))

emType = ("embellished", "norm_01", "norm_02", "unrelated_01", "unrelated_02")
# Cycle through all filenames and place as you go
for i in graphTypes:
    print ("g", i)
    for j in data[i]:
        # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
        for ind, k in enumerate(emType):
            for x in fileNames:
                if i in x and j["key"] in x and k in x:
                    print ("iCaught: ", x)
                    print ("iCaught a : ", j["key"])
                    j["imagePath"][ind] = "modules/graphQuestions/graphImages/final_color/"+x
                    j["imagePathBW"].append("modules/graphQuestions/graphImages/final_bw/"+x)
                    allImages.append("modules/graphQuestions/graphImages/final_color/"+x)
                    # j["newPath"] = j["newPath"] + [x]
                else:
                    print("notCaught: ", j["key"], x)

# Get base files
# In future might be better to make naming convention rather than using the file name
for i in graphTypes:
    print ("g", i)
    for j in data[i]:
        # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
        for ind, k in enumerate(emType):
            for x in baseNames:
                if i in x and j["key"] in x and k in x:
                    print ("iCaught: ", x)
                    print ("iCaught a : ", j["key"])
                    j["basePath"].append("modules/graphTheme/chartBase/"+x)
                else:
                    print("notCaught: ", j["key"], x)

# Getting interact files for lines
inType = ("interact_00", "interact_01", "interact_02")
#  For line interact files.
for x in interactNames:
    # for i in graphTypes:
    if graphTypes[0] in x:
        # pprint (data[i])
        for j in data[graphTypes[0]]:
            if j["key"] in x:
                # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
                for ind, k in enumerate(inType):
                    if k in x:
                        img = cv2.imread("./graphImages/interact/"+x,1)
                        if ind == 0:
                            j["interact"]["imageDim"]= (img.shape[1], img.shape[0])
                        if ind > 1:
                            j["interact"]["imagePath"].append("")
                            j["interact"]["iconDim"] = (img.shape[1], img.shape[0])
                            # j["interact"]["imageDim"].append(tuple())
                            j["interact"]["withIcon"] = True
                            # img = cv2.imread("./graphImages")
                        # print ("iCaught a : ", j["key"])
                        j["interact"]["imagePath"][ind] = "modules/graphQuestions/graphImages/interact/"+x
                        allImages.append("modules/graphQuestions/graphImages/interact/"+x)
                        img = cv2.imread("./graphImages/interact/"+x,1)
                        print ("img", x)
                        # print (img)
                        # j["newPath"] = j["newPath"] + [x]
            else:
                print("notCaught: ", j["key"], x)

# pies!
inType = ("interact_00", "interact_01", "interact_02", "interact_03", "interact_04")
#  For line interact files.
for x in interactNames:
    # for i in graphTypes:
    if graphTypes[1] in x:
        # pprint (data[i])
        for j in data[graphTypes[1]]:
            if j["key"] in x:
                # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
                for ind, k in enumerate(inType):
                    if k in x:
                        # getting the image dim for the first icon?
                        if ind == 0:
                            img = cv2.imread("./graphImages/interact/"+x,1)
                            # print ("img", x)
                            j["interact"]["imageDim"] = (img.shape[1], img.shape[0])
                        img = cv2.imread("./graphImages/interact/"+x, 1)
                        j["interact"]["imagePath"].append({"path":"modules/graphQuestions/graphImages/interact/"+x, "iconDim":(img.shape[1], img.shape[0])})
                        allImages.append("modules/graphQuestions/graphImages/interact/"+x)
                        if len(j["interact"]["colorArray"])!=0:
                            j["interact"]["withIcon"] = True
            else:
                print("notCaught: ", j["key"], x)

# Getting the interact image files for the bars
inType = ("interact_00", "interact_01", "interact_02", "interact_03", "interact_04", "interact_05", "interact_06")
#  For line interact files.
for x in interactNames:
    # for i in graphTypes:
    if graphTypes[2] in x:
        # pprint (data[i])
        for j in data[graphTypes[2]]:
            if j["key"] in x:
                # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
                for ind, k in enumerate(inType):
                    if k in x:
                        if ind == 0:
                            img = cv2.imread("./graphImages/interact/"+x,1)
                            # print ("img", x)
                            j["interact"]["imageDim"] = (img.shape[1], img.shape[0])
                        if ind == 1:
                            img = cv2.imread("./graphImages/interact/"+x,1)
                            j["interact"]["barDim"] = (img.shape[1], img.shape[0])
                        j["interact"]["imagePath"].append("modules/graphQuestions/graphImages/interact/"+x)
                        allImages.append("modules/graphQuestions/graphImages/interact/"+x)
            else:
                print("notCaught: ", j["key"], x)
for j in data[graphTypes[2]]:
    j["interact"]["numBars"] = len(j["interact"]["imagePath"])-1


#--------------------BW Interact-------------------#
# BW INTERACT FOR LINES!
inType = ("interact_bw_00", "interact_bw_01", "interact_bw_02")
for x in interactBWNames:
    if graphTypes[0] in x:
        for j in data[graphTypes[0]]:
            if j["key"] in x:
                for ind, k in enumerate(inType):
                    if k in x:
                        # if ind > 1:
                        j["interact"]["imagePathBW"].append("")
                        j["interact"]["imagePathBW"][ind] = "modules/graphQuestions/graphImages/interact_bw/"+x
                        allImages.append("modules/graphQuestions/graphImages/interact_bw/"+x)
            # else:
            #     print("notCaught: ", j["key"], x)

# BW INTERACT FOR PIES!
inType = ("interact_bw_00", "interact_bw_01", "interact_bw_02", "interact_bw_03", "interact_bw_04")
for x in interactBWNames:
    if graphTypes[1] in x:
        for j in data[graphTypes[1]]:
            if j["key"] in x:
                for ind, k in enumerate(inType):
                    if k in x:
                        img = cv2.imread("./graphImages/interact_bw/"+x, 1)
                        print ('xPIE-', x)
                        j["interact"]["imagePathBW"].append({"path":"modules/graphQuestions/graphImages/interact_bw/"+x, "iconDim":(img.shape[1], img.shape[0])})
                        allImages.append("modules/graphQuestions/graphImages/interact_bw/"+x)
            # else:
            #     print("notCaught: ", j["key"], x)

# BW INTERACT FOR BARS
inType = ("interact_bw_00", "interact_bw_01", "interact_bw_02", "interact_bw_03", "interact_bw_04", "interact_bw_05", "interact_bw_06")
for x in interactBWNames:
    if graphTypes[2] in x:
        for j in data[graphTypes[2]]:
            if j["key"] in x:
                for ind, k in enumerate(inType):
                    if k in x:
                        j["interact"]["imagePathBW"].append("modules/graphQuestions/graphImages/interact_bw/"+x)
                        allImages.append("modules/graphQuestions/graphImages/interact_bw/"+x)
            # else:
            #     print("notCaught: ", j["key"], x)

# -----SAVING THE DATA!!!------#


# Print the new object
print("newData is: ")
for i in data:
    for j in data[i]:
        pprint(j["imagePath"])

print("\n")
pprint(data["line"][0]["imagePath"][2])
# pprint(data["bar"])

# Write the new object
# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch06s02.html
# Writing JSON data
with open('data.json', 'w') as f:
     json.dump(data, f, indent=4)

with open('allImages.json', 'w') as aI:
    json.dump(allImages, aI)
