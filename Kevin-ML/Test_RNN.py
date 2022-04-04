#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

trainX = np.load("trainX.npy", allow_pickle=True)
trainY = np.load("trainY.npy", allow_pickle=True)
testX = np.load("testX.npy", allow_pickle=True)
testY = np.load("testY.npy", allow_pickle=True)

trainX = tf.convert_to_tensor(trainX, dtype=tf.float32)
trainY = tf.convert_to_tensor(trainY, dtype=tf.float32)
testX = tf.convert_to_tensor(testX, dtype=tf.float32)
testY = tf.convert_to_tensor(testY, dtype=tf.float32)

model = tf.keras.models.load_model('trained_model')
results = model.evaluate(trainX, trainY, batch_size=128)
print(results)