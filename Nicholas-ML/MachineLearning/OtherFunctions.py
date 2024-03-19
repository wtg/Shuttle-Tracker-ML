def read_file(file_name):
    AllData = None
    with open(file_name, 'r') as fileRead:
        for line in fileRead:
            splitUp = line.split(",")
            if (AllData == None):
                AllData = [[] for elem in splitUp ]
            for i in range(len(splitUp)):
                AllData[i].append(int(splitUp[i].replace("\n","")))
    return AllData

def Get_All_Points():
    Points = []
    with open("../CoordinatesToIntWork/PointsOutput.txt", 'r') as file:
        for line in file:
            line = line.replace("\n","")
            x = float(line.split(",")[0])
            y = float(line.split(",")[1])

            Points.append((x,y))
    return Points

