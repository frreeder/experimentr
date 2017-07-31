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
        # j["newPath"]=[]
        # https://stackoverflow.com/questions/521674/initializing-a-list-to-a-known-number-of-elements-in-python
        j["imagePath"]=["modules/graphQuestions/graphImages/color/rangerPoseGreen.png"] * 5
        pprint(j)
        print(j["title"])

# Adding an imagePath for the lines
for j in data["line"]:
    j["interact"]["imagePath"]=["modules/graphQuestions/graphImages/color/rangerPoseGreen.png"] * 2
    j["interact"]["imageDim"]=[tuple()]*2
    j["interact"]["withIcon"]= False
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/line_data_"+j["key"]+".csv"

# Adding an imagePath for the lines
for j in data["pie"]:
    # j["interact"]["imagePath"]=["modules/graphQuestions/graphImages/color/rangerPoseGreen.png"] * 2
    # j["interact"]["imageDim"]=tuple()
    j["interact"]["withIcon"]= False
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/pie_data_"+j["key"]+".csv"

# Adding an imagePath for the lines
for j in data["bar"]:
    j["interact"]["dataPath"]="modules/graphInteract/csvFiles/bar_data_"+j["key"]+".csv"

# for i in data:
#     for j in data[i]:
#         apple=2

# pprint(data)
pprint(data["line"][0])

# I can a list of the directory image files.

F = open("./graphList.json", "r")
print ("pot")
# print (F.read())

# fileNames = filter(lambda x: x.endswith('.txt'), os.listdir('mydir'))
fileNames = os.listdir("./graphImages/color")
print("fileNames", fileNames)

interactNames = os.listdir("./graphImages/interact")

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
# I need to get the key of each file and check the image list... should make a dictionary ...
# If path includes line => go lines, if includes embellished => 0 or something like that
# Cycle through all filenames and place as you go
for x in fileNames:
    print ("xNew", x)
    print ("\n")
    for i in graphTypes:
        print ("g", i)
        if i in x:
            print ("iCaught: ", x)
            # pprint (data[i])
            for j in data[i]:
                if j["key"] in x:
                    # https://stackoverflow.com/questions/15684605/python-for-loop-get-indexs
                    for ind, k in enumerate(emType):
                        if k in x:
                            print ("iCaught a : ", j["key"])
                            j["imagePath"][ind] = "modules/graphQuestions/graphImages/color/"+x
                            # j["newPath"] = j["newPath"] + [x]
                else:
                    print("notCaught: ", j["key"], x)

inType = ("interact_01", "interact_02", "interact_03")
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
                        if ind > 1:
                            j["interact"]["imagePath"].append("")
                            j["interact"]["imageDim"].append(tuple())
                            j["interact"]["withIcon"] = True
                        # print ("iCaught a : ", j["key"])
                        j["interact"]["imagePath"][ind] = "modules/graphQuestions/graphImages/interact/"+x
                        img = cv2.imread("./graphImages/interact/"+x,1)
                        print ("img", x)
                        # print (img)
                        j["interact"]["imageDim"][ind] = (img.shape[1], img.shape[0])
                        # j["newPath"] = j["newPath"] + [x]
            else:
                print("notCaught: ", j["key"], x)

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
                        if ind == 0:
                            img = cv2.imread("./graphImages/interact/"+x,1)
                            # print ("img", x)
                            j["interact"]["imageDim"] = (img.shape[1], img.shape[0])
                        j["interact"]["imagePath"].append({"path":"modules/graphQuestions/graphImages/interact/"+x})
                        if len(j["interact"]["colorArray"])!=0:
                            j["interact"]["withIcon"] = True
            else:
                print("notCaught: ", j["key"], x)

# Getting the interact image files for the bars
inType = ("interact_01", "interact_02")
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
                        j["interact"]["imagePath"].append("modules/graphQuestions/graphImages/interact/"+x)
            else:
                print("notCaught: ", j["key"], x)




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
     json.dump(data, f)
