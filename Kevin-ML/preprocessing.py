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
        return np.array([self.lat, self.lon])

if __name__ == "__main__":
	random.seed()
	filename = input("Enter datafile(csv): ")
    #Read in and split data into user data(has uniform timestep) and system data
	file = open(filename)
	csvreader = csv.reader(file)
	user_data, sys_data = [], []
	for row in csvreader:
		if row[4] == 'user':
			user_data.append(Datapoint(row[0], row[1], row[2], row[3], row[4]))
		else:
			sys_data.append(Datapoint(row[0], row[1], row[2], row[3], row[4]))

	#Split user data into trips - currently there are 1691 trips from early Spring 2022 data
	current, trips = {}, []
	for i in range(len(user_data)):
		current_ID = user_data[i].ID
		if i != 0:
			if current_ID not in current:
				current[current_ID] = [user_data[i].time, [user_data[i].formatted()]]
			else:
				#Maintain uniform time interval of 5 seconds
				if (user_data[i].time - current[current_ID][0]) == 5:
					current[current_ID][1].append(user_data[i].formatted())
					current[current_ID][0] = user_data[i].time
				else:
					if len(current[current_ID][1]) > 1:
						trips.append(current[current_ID][1])
					current[current_ID] = [user_data[i].time, [user_data[i].formatted()]]
		else:
			current[user_data[i].ID] = [user_data[i].time, [user_data[i].formatted()]]
	
	#See if there are any system data points that have uniform time interval of 5 seconds
	#As of early Spring 2022 data set, 139 trips meet this criteria
	for i in range(len(sys_data)):
		current_ID = sys_data[i].ID
		if i != 0:
			if current_ID not in current:
				current[current_ID] = [sys_data[i].time, [sys_data[i].formatted()]]
			else:
				#Maintain uniform time interval of 5 seconds
				if (sys_data[i].time - current[current_ID][0]) == 5:
					current[current_ID][1].append(sys_data[i].formatted())
					current[current_ID][0] = sys_data[i].time
				else:
					if len(current[current_ID][1]) > 1:
						trips.append(current[current_ID][1])
					current[current_ID] = [sys_data[i].time, [sys_data[i].formatted()]]
		else:
			current[sys_data[i].ID] = [sys_data[i].time, [sys_data[i].formatted()]]

	#Split longer trips into trips of length 10 with overlap (to have more data points)
	newtrips = []
	for i in range(len(trips)):
		if len(trips[i]) == 6:
			newtrips.append(trips[i])
		elif len(trips[i]) > 6:
			for j in range(len(trips[i])-6):
				newtrips.append(trips[i][j:j+6])
	trips = newtrips

	#Split the total trips into training and testing set
	indices = set()
	while len(indices) < round(len(trips)/10):
		indices.add(random.randint(0, len(trips)))

	trainX, trainY, testX, testY = [], [], [], []
	for i in range(len(trips)):
		if i in indices:
			testX.append(trips[i][:len(trips[i])-1])
			testY.append(trips[i][-1])
		else:
			trainX.append(trips[i][:len(trips[i])-1])
			trainY.append(trips[i][-1])

	print(len(trainX), len(trainY), len(testX), len(testY))

	trainX = np.asanyarray(trainX, dtype=object)
	trainY = np.asanyarray(trainY, dtype=object)
	testX = np.asanyarray(testX, dtype=object)
	testY = np.asanyarray(testY, dtype=object)
	
	np.save("trainX.npy", trainX)
	np.save("trainY.npy", trainY)
	np.save("testX.npy", testX)
	np.save("testY.npy", testY)