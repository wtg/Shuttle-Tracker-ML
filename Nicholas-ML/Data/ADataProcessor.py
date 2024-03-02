import sys
import os
if (len(sys.argv) < 3):
    print("Have the command line arguments be the file you want to read from and the folder you want to write to as.")
    exit(1)
filename = sys.argv[1]
folder = sys.argv[2]
mapOfData = {}

try:
    os.mkdir(folder)
except Exception as e:
    folder = folder

shuttleBusNumberIndex = input("What is the index of the shuttle bus number (1 is first column)?")
if (shuttleBusNumberIndex == ""):
    shuttleBusNumberIndex = 1
else:
    shuttleBusNumberIndex = int(shuttleBusNumberIndex)

def StringTimeToIntTime(str):
    date = str.split(" ")[0].split("-")
    time = str.split(" ")[1].split(":")
    year, month, day = int(date[0]), int(date[1]), int(date[2])
    hour, minute, second = int(time[0]), int(time[1]), int(time[2])
    return (year - 1970) * 31536000 + (month - 1) * 2592000 + (day - 1) * 86400 + hour * 3600 + minute * 60 + second

indexForTimeInArray = -1
with open(filename, 'r') as fileRead:
    for line in fileRead:
        splitUp = line.split(",")
        busNumber = splitUp[shuttleBusNumberIndex-1]
        temp = []
        if busNumber not in mapOfData:
            mapOfData[busNumber] = []

        for i in range(len(splitUp)):
            if (splitUp[i] == "user" or splitUp[i] == "system" or splitUp[i] == "user\n" or splitUp[i] == "system\n"):
                continue
            if (i == shuttleBusNumberIndex-1):
                continue
            if (splitUp[i].find("+") != -1 and splitUp[i].find(":") != -1 and splitUp[i].find("-") != -1):
                temp.append(StringTimeToIntTime(splitUp[i]))
                indexForTimeInArray = len(temp)-1
                continue
            temp.append(splitUp[i])
        mapOfData[busNumber].append(temp)

def custom_sort(item):
    return item[indexForTimeInArray]

# Adds outputs parameters
for key in mapOfData:
    mapOfData[key] = sorted(mapOfData[key], key=custom_sort)
    for i in range(len(mapOfData[key])):
        if (i == 0):
            continue
        nextPos = mapOfData[key][i][0]
        timeDif = mapOfData[key][i][1] - mapOfData[key][i-1][1]
        mapOfData[key][i-1].append(nextPos)
        mapOfData[key][i-1].append(timeDif)
    mapOfData[key] = mapOfData[key][0:-1]

with open("./" + folder + "/AllBusses.csv", 'w') as fileAll:       
    for key in mapOfData:
        mapOfData[key] = sorted(mapOfData[key], key=custom_sort)
        with open("./" + folder + "/bus" + key + ".csv", 'w') as file1:    
            for i in range(len(mapOfData[key])):
                fileAll.write(key)
                for j in range(len(mapOfData[key][i])):
                    fileAll.write(","+str(mapOfData[key][i][j]))
                    if (j != 0):
                        file1.write(",")
                    file1.write(str(mapOfData[key][i][j]))
                fileAll.write("\n")
                file1.write("\n")