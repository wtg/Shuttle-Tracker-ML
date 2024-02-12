import sys
from sklearn.neighbors import KDTree
if (len(sys.argv) < 3):
    print("Have the command line arguments be the file you want to read from and the file you want to write to as.")
    exit()
fileToReadFrom = sys.argv[1]
fileToWriteTo = sys.argv[2]
#ask what column is on input position
columnOfInterest = int(input("What column has the position represented as an int (first column is 1)? "))

#Read all points from the output of "PointsOnRouteMaker.py"
Points = []
with open("../CoordinatesToIntWork/PointsOutput.txt", 'r') as file:
    for line in file:
        line = line.replace("\n","")
        x = line.split(",")[0]
        y = line.split(",")[1]

        Points.append((x,y))

#empty file
with open(fileToWriteTo, 'w') as fileWrite:
    pass

#Read all data points from first command line argument
with open(fileToReadFrom, 'r') as fileRead:
    for line in fileRead:
        doubleCoords = [0,0]
        found = 0
        splitUp = line.split(",")
        for i in range(len(splitUp)):
            #When on column that has one input position (asked for before), replace it with position
            if ((i + 1) == columnOfInterest):
                coords = Points[int(splitUp[i])]
                splitUp[i] = coords[0]
                splitUp.insert(i, coords[1])

        #write to file
        with open(fileToWriteTo, 'a') as fileWrite:
            stringOfLine = ""
            for item in splitUp:
                if (item != ""):
                    item = str(item).replace("\n", "")
                    stringOfLine += str(item) + ","
            fileWrite.write(stringOfLine[0:-1]+"\n")