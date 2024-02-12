import sys
from sklearn.neighbors import KDTree
if (len(sys.argv) < 3):
    print("Have the command line arguments be the file you want to read from and the file you want to write to as.")
    exit()
fileToReadFrom = sys.argv[1]
fileToWriteTo = sys.argv[2]

# Find nearest integer point from coordinates given
def nearest_point(target):
    global tree, Points
    dist, ind = tree.query([target], k=1)
    return ind[0][0]

#Read all points from the output of "PointsOnRouteMaker.py"
Points = []
with open("../CoordinatesToIntWork/PointsOutput.txt", 'r') as file:
    for line in file:
        line = line.replace("\n","")
        x = line.split(",")[0]
        y = line.split(",")[1]

        Points.append((x,y))
tree = KDTree(Points)

#empty file
with open(fileToWriteTo, 'w') as fileWrite:
    pass

#Read all data points from first command line argument
with open(fileToReadFrom, 'r') as fileRead:
    for line in fileRead:
        doubleCoords = [0,0]
        found = 0
        splitUp = line.split(",")
        #Go through all data in row
        for i in range(len(splitUp)):
            #If a coordinate, store it in array
            if (splitUp[i][0:3] == "42."):
                doubleCoords[1] = float(splitUp[i])
            if (splitUp[i][0:4] == "-73."):
                doubleCoords[0] = float(splitUp[i])

            # If found both of them, replace the points and replace it with an int data type
            if (splitUp[i][0:3] == "42." or splitUp[i][0:4] == "-73."):
                found += 1
                if (found == 1):
                    splitUp[i] = ""
                if (found == 2):
                    splitUp[i] = nearest_point((doubleCoords[0], doubleCoords[1]))

        #Write to output file
        with open(fileToWriteTo, 'a') as fileWrite:
            stringOfLine = ""
            for item in splitUp:
                if (item != ""):
                    item = str(item).replace("\n", "")
                    stringOfLine += str(item) + ","
            fileWrite.write(stringOfLine[0:-1]+"\n")
        

        

# print(nearest_point((-73.67644, 42.73037)))
# print(Points[nearest_point((-73.67644, 42.73037))])