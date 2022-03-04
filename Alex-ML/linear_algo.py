import numpy as np
import pandas as pd
from numpy.polynomial import polynomial as p
import matplotlib.pyplot as plt
import csv


csv_file = open('Data_session.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter = ',')

csv_list = list(csv_reader)


session = '0'
ID = '85'

result = []
x = []
y = []

for lines in csv_list:
    #print(x)
    if lines[5] == session and lines[0] == ID:
        x.append(float(lines[1]))
        y.append(float(lines[2]))
        

    elif lines[0] == ID and lines[5] != session and lines[1] != 'Latitude' and lines[2] != 'Longitude':
        #print(x)
        if(len(x) == 1):
            m = 0
            b = 0
            result.append([m, b])
            session = lines[5]
            x = []
            y = []
            x.append(float(lines[1]))
            y.append(float(lines[2]))
        else:
            m, b = np. polyfit(x, y, 1)
            result.append([m, b])
            session = lines[5]
            x = []
            y = []
            x.append(float(lines[1]))
            y.append(float(lines[2]))
        

    elif lines[0] != ID and lines[1] != 'Latitude' and lines[2] != 'Longitude':
        if(len(x) == 1):
            m = 0
            b = 0
            result.append([m, b])
            session = 0
            ID = lines[0]
            x = []
            y = []
            x.append(float(lines[1]))
            y.append(float(lines[2]))
        else:
            m, b = np. polyfit(x, y, 1)
            result.append([m, b])
            session = 0
            ID = lines[0]
            x = []
            y = []
            x.append(float(lines[1]))
            y.append(float(lines[2]))
            


# print(x)
# print(y)
print(result)
