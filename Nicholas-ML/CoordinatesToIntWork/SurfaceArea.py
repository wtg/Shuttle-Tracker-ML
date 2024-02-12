import math
import sys

# Calcuates the distance between two lines from the file
def distanceFormula(line1, line2):
    x1 = float(line1.split(',')[0])
    y1 = float(line1.split(',')[1])

    x2 = float(line2.split(',')[0])
    y2 = float(line2.split(',')[1])

    return math.sqrt(((y2-y1)**2) + ((x2-x1)**2))

# Reads a shuttle route file and returns the total distance of that route
def readFileAndGetDistance(filename):
    prevLine = ""
    totalDistance = 0
    with open(filename, 'r') as file:
        for line in file:
            if (prevLine != ""):
                totalDistance += distanceFormula(prevLine, line)
            prevLine = line
    return totalDistance

# Get all surface areas from command line arguments
Distances = []
i = 1
while (i < len(sys.argv)):
    Distances.append(readFileAndGetDistance('./Coordinates/' + sys.argv[i]))
    i += 1

# Prints all surface areas seperated by a space
toPrint = ""
for element in Distances:
    toPrint += str(element) + " "
print(toPrint)