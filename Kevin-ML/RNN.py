#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

trainX = np.load("trainX.npy", allow_pickle=True)
trainY = np.load("trainY.npy")
testX = np.load("testX.npy", allow_pickle=True)
testY = np.load("testY.npy")

trainX = tf.ragged.constant(trainX, dtype=tf.float32)
trainY = tf.convert_to_tensor(trainY, dtype=tf.float32)
testX = tf.ragged.constant(testX, dtype=tf.float32)
testY = tf.convert_to_tensor(testY, dtype=tf.float32)

padded_trainX = trainX.to_tensor(0.)
padded_testX = testX.to_tensor(0.)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(64, return_sequences=False))
model.add(tf.keras.layers.Dense(3, activation='linear', name='output'))
model.compile(loss='mean_squared_error', optimizer='adam')


model.fit(padded_trainX, trainY, batch_size=10, epochs=10, validation_split=0.05)
model.summary()