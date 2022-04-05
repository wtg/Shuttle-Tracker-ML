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

model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(128))
model.add(tf.keras.layers.Dense(2))

model.compile(optimizer='adam', loss='MSE', metrics = ['MeanAbsolutePercentageError'])

output = model.fit(trainX, trainY, batch_size=64, epochs=30, validation_data=(testX, testY))
model.save("trained_model")
x_axis = range(30)
loss = output.history['loss']
val_loss = output.history['val_loss']


plt.figure(0)
plt.plot(x_axis, loss)
plt.savefig('train_loss.png')
plt.figure(1)
plt.plot(x_axis, val_loss)
plt.savefig('val_loss.png')

'''
#Convert numpy arrays to tensors
trainX = tf.ragged.constant(trainX, dtype=tf.float32)
trainY = tf.ragged.constant(trainY, dtype=tf.float32)
testX = tf.ragged.constant(testX, dtype=tf.float32)
testY = tf.ragged.constant(testY, dtype=tf.float32)

lengths = {}
for trip in trainX:
	if trip.shape[0] not in lengths:
		lengths[trip.shape[0]] = 1
	else:
		lengths[trip.shape[0]] += 1
keys = lengths.keys()
keys = sorted(keys)
for key in keys:
	print(key, lengths[key])
'''