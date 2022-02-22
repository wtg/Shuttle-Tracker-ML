#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

trainX = np.load("trainX.npy", allow_pickle=True)
trainY = np.load("trainY.npy")
testX = np.load("testX.npy", allow_pickle=True)
testY = np.load("testY.npy")

trainX = tf.ragged_constant(trainX, dtype=tf.float32)
trainY = tf.ragged_constant(trainY, dtype=tf.float32)
testX = tf.ragged_constant(testX, dtype=tf.float32)
testY = tf.ragged_constant(testY, dtype=tf.float32)

model = tf.keras.Sequential()
