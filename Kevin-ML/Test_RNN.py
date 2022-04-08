#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import haversine
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

trainX = np.load("trainX.npy", allow_pickle=True)
trainY = np.load("trainY.npy", allow_pickle=True)
testX = np.load("testX.npy", allow_pickle=True)
testY = np.load("testY.npy", allow_pickle=True)

trainX = np.vstack((trainX, testX))
trainY = np.vstack((trainY, testY))
x, y = 0, 0
total = len(trainX) * len(trainX[0]) + len(trainY)
for i in range(len(trainX)):
    x += trainY[i][0]
    y += trainY[i][1]
    for j in range(len(trainX[i])):
        x += trainX[i][j][0]
        y += trainX[i][j][1]
x /= total
y /= total

trainX = tf.convert_to_tensor(trainX, dtype=tf.float32)
trainY = tf.convert_to_tensor(trainY, dtype=tf.float32)

model = tf.keras.models.load_model('trained_model')
results = model.evaluate(trainX, trainY, batch_size=128)
print(results)
err = results[1]/100
x2, y2 = x * (1-err), y * (1-err)
dist = haversine.haversine((x, y), (x2, y2))*1000
print("Average error in meters: ", dist)