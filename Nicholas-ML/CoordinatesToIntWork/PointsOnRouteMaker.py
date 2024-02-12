import subprocess
import math
import sys
fileToWriteTo = 'PointsOutput.txt'
fileToWriteToKML = 'PointsOutput.kml'
kmlPointNum = 0

#Empty both files
with open(fileToWriteTo, 'w') as file:
    pass
with open(fileToWriteToKML, 'w') as file:
    pass
    file.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>Untitled layer</name>')

#Calcualtes distance between two points
def distanceFormula(line1, line2):
    x1 = float(line1.split(',')[0])
    y1 = float(line1.split(',')[1])

    x2 = float(line2.split(',')[0])
    y2 = float(line2.split(',')[1])

    return math.sqrt(((y2-y1)**2) + ((x2-x1)**2))

#Writes to new data point in appropriate format for both files
def writeToFiles(x,y):
    global kmlPointNum, fileToWriteTo, fileToWriteToKML
    with open(fileToWriteTo, 'a') as file:
        file.write(str(x)+","+str(y)+"\n")
    with open(fileToWriteToKML, 'a') as file:
        file.write('<Placemark><name>Point '+str(kmlPointNum)+'</name><styleUrl>#icon-1899-0288D1-nodesc</styleUrl><Point><coordinates>'+str(x)+","+str(y)+",0"+'</coordinates></Point></Placemark>')
    kmlPointNum += 1

#Assaigns all points directly from the route given
def AssignPointsLazy(fileToReadFrom):
    with open(fileToReadFrom, 'r') as file:
        for line in file:
            writeToFiles(line.split(',')[0], line.split(',')[1])

#Assaigns all points "distancePerPoint" away from each other
def AssignPoints(fileToReadFrom):
    global fileToWriteTo, distancePerPoint
    prevLine = ""
    distanceRemaining = distancePerPoint
    with open(fileToReadFrom, 'r') as file:
        for line in file:
            if (prevLine != ""):
                lineSize = distanceFormula(prevLine, line)
                while (distanceRemaining - lineSize < 0): #If traveled "distancePerPoint" distance
                    x1 = float(prevLine.split(',')[0])
                    y1 = float(prevLine.split(',')[1])
                    x2 = float(line.split(',')[0])
                    y2 = float(line.split(',')[1])
                    #Gets angle to move in for next point
                    angle = math.atan((y2-y1)/(0.00000001))
                    if ((x2-x1) != 0):
                        angle = math.atan(math.fabs(y2-y1)/math.fabs(x2-x1))
                    angle = angle % (math.pi / 2)

                    #Move the appropriate distance in x and y direction
                    if (x2 > x1):
                        newX = x1+(math.cos(angle)*distanceRemaining)
                    else:
                        newX = x1-(math.cos(angle)*distanceRemaining)
                    if (y2 > y1):
                        newY = y1+(math.sin(angle)*distanceRemaining)
                    else:
                        newY = y1-(math.sin(angle)*distanceRemaining)
                    #write it to the files
                    writeToFiles(newX, newY)

                    #Recaulcate the distance the remainder of this line has
                    distanceRemaining = distancePerPoint
                    prevLine = str(newX)+","+str(newY)+"\n"
                    lineSize = distanceFormula(prevLine, line)
                distanceRemaining -= lineSize
            prevLine = line


# Run SurfaceArea.py
subprocessArray = ['python', 'SurfaceArea.py']
for i in range(1, len(sys.argv)):
    subprocessArray.append(sys.argv[i])
result = subprocess.run(subprocessArray, capture_output=True, text=True)
SurfaceAreaResult = result.stdout.replace("\n","")

# Get total distance
TotalDistance = 0
for i in range(1, len(sys.argv)):
    TotalDistance += float(SurfaceAreaResult.split(" ")[i-1])


amtPoints = float(input("How many points do you want? ")) # 1800 is good amount
distancePerPoint = float(TotalDistance / amtPoints)
for i in range(1, len(sys.argv)):
    AssignPoints('./Coordinates/' + sys.argv[i])

#Close file properly
with open(fileToWriteToKML, 'a') as file:
    file.write('</Document></kml>')
