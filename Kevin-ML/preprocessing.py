#!/usr/bin/env python
import csv
import datetime
import random
import numpy
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
        return numpy.array([self.lat, self.lon, self.time])

    def timestamp(self):
        return numpy.array([self.time])

    def loc(self):
        return numpy.array([self.lat, self.lon])

if __name__ == "__main__":
   random.seed()
    
   file = open("Data.csv")
   csvreader = csv.reader(file)
   rows = []
   for row in csvreader:
       rows.append(Datapoint(row[0], row[1], row[2], row[3], row[4]))
   trips = []
   for i in range(len(rows)-1):
       timeDiff = rows[i+1].dt - rows[i].dt
       if int(str(timeDiff).split(":")[-2]) < 15:
           trips.append((numpy.hstack((rows[i].formatted(), rows[i+1].timestamp())), rows[i+1].loc()))

   indices = set()
   while len(indices) < 4300:
       indices.add(random.randint(0, len(trips)))
    
   trainX, trainY, testX, testY, i = [], [], [], [], 0
   while i < len(trips):
       if i in indices:
           testX.append(trips[i][0])
           testY.append(trips[i][1])
       else:
           trainX.append(trips[i][0])
           trainY.append(trips[i][1])
       i += 1
       
   trainX = tf.convert_to_tensor(trainX, dtype=tf.float32)
   trainY = tf.convert_to_tensor(trainY, dtype=tf.float32)
   testX = tf.convert_to_tensor(testX, dtype=tf.float32)
   testY = tf.convert_to_tensor(testY, dtype=tf.float32)

   data_input = tf.keras.Input(shape=(4,))
   layer1 = tf.keras.layers.Dense(3, activation="relu")
   x = layer1(data_input)
   layer2 = tf.keras.layers.Dense(3, activation="relu")
   x = layer2(x)
   layer3 = tf.keras.layers.Dense(3, activation="relu")
   x = layer3(x)
   data_output = tf.keras.layers.Dense(2)(x)
   model1 = tf.keras.Model(inputs = data_input, outputs = data_output, name="Neural_Net_1")
   model1.summary()
   
   model1.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=tf.keras.optimizers.Adadelta(), metrics=[tf.keras.metrics.MeanAbsoluteError()])
   
   history = model1.fit(trainX, trainY, epochs = 5)
   test_scores = model1.evaluate(testX, testY)
   print("Test Loss", test_scores[0])
   print("Test accuracy", test_scores[1])
