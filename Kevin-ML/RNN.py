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
num_epoch = int(input("Enter number of epochs for model: "))
output = model.fit(trainX, trainY, batch_size=64, epochs=num_epoch, validation_data=(testX, testY))
model.save("trained_model")
#model.summary()
x_axis = range(num_epoch)
loss = output.history['loss']
acc = output.history['mean_absolute_percentage_error']
val_loss = output.history['val_loss']
val_acc = output.history['val_mean_absolute_percentage_error']


plt.figure(0)
plt.plot(x_axis, loss)
plt.figure(0)
plt.plot(x_axis, val_loss)
plt.savefig('loss.png')
plt.figure(1)
plt.plot(x_axis, acc)
plt.figure(1)
plt.plot(x_axis, val_acc)
plt.savefig('err.png')