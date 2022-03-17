#!/usr/bin/env python
import csv
import datetime
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

class Datapoint:
    def __init__(self, idnum, latitude, longitude, dtime, source):
        self.ID = int(idnum)
        self.lat = float(latitude)
        self.lon = float(longitude)
        self.dt = datetime.datetime(int(dtime[:4]), int(dtime[5:7]), \
                int(dtime[8:10]), int(dtime[11:13]), \
                int(dtime[14:16]), int(dtime[17:19]))
        self.time = 24 * 60 * int(dtime[11:13]) + 60 * int(dtime[14:16]) + int(dtime[17:19])
        self.source = source

    def __repr__(self):
        return str(self.ID) + " " +  str(self.lat) + ", " + \
                str(self.lon) + " " + str(self.dt) + " " + self.source + "\n"
    

    def formatted(self):
        return np.array([self.lat, self.lon, self.time])

if __name__ == "__main__":
	random.seed()
    
	file = open("Data.csv")
	csvreader = csv.reader(file)
	rows = []
	for row in csvreader:
		rows.append(Datapoint(row[0], row[1], row[2], row[3], row[4]))

	trips = []
	currentTimes, currentTrips = {}, {}
	for dPoint in rows:
		cID = dPoint.ID
		if cID not in currentTrips:
			currentTrips[cID] = [dPoint.formatted()]
		else:
			timeDiff = dPoint.dt - currentTimes[cID].dt
			if int(str(timeDiff).split(":")[-2]) > 15:
				trips.append(currentTrips[cID])
				currentTrips[cID] = [dPoint.formatted()]
			else:
				currentTrips[cID].append(dPoint.formatted())
		currentTimes[cID] = dPoint
	for remainder in currentTrips:
		trips.append(currentTrips[remainder])

	indices = set()
	while len(indices) < round(len(trips)/10):
		indices.add(random.randint(0, len(trips)))
	trainX, trainY, testX, testY, i = [], [], [], [], 0
	
	while i < len(trips):
		if i in indices and len(trips[i]) > 1:
			testX.append(trips[i][:len(trips[i])-1])
			testY.append(trips[i][len(trips[i])-1])
		elif i not in indices and len(trips[i]) > 1:
			trainX.append(trips[i][:len(trips[i])-1])
			trainY.append(trips[i][len(trips[i])-1])
		i += 1
    
	trainX = np.asanyarray(trainX, dtype=object)
	testX = np.asanyarray(testX, dtype=object)
	
	np.save("trainX.npy", trainX)
	np.save("trainY.npy", trainY)
	np.save("testX.npy", testX)
	np.save("testY.npy", testY)