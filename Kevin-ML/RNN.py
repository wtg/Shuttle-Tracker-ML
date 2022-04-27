#!/usr/bin/env python
import numpy as np
import tensorflow as tf
import os
import matplotlib.pyplot as plt
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

#Autoregressive model based on Tensorflow example
class FeedBack(tf.keras.Model):
  def __init__(self, units, out_steps):
	  super().__init__()
	  self.out_steps = out_steps
	  self.units = units
	  self.lstm_cell = tf.keras.layers.LSTMCell(units)
	  # Also wrap the LSTMCell in an RNN to simplify the `warmup` method.
	  self.lstm_rnn = tf.keras.layers.RNN(self.lstm_cell, return_state=True)
	  self.dense = tf.keras.layers.Dense(2)

  def warmup(self, inputs):
	  # inputs.shape => (batch, time, features)
	  # x.shape => (batch, lstm_units)
	  x, *state = self.lstm_rnn(inputs)

	  # predictions.shape => (batch, features)
	  prediction = self.dense(x)
	  return prediction, state

  def call(self, inputs, training=None):
	  # Use a TensorArray to capture dynamically unrolled outputs.
	  predictions = []
	  # Initialize the LSTM state.
	  prediction, state = self.warmup(inputs)

	  # Insert the first prediction.
	  predictions.append(prediction)

	  # Run the rest of the prediction steps.
	  for n in range(1, self.out_steps):
	    # Use the last prediction as input.
	    x = prediction
	    # Execute one lstm step.
	    x, state = self.lstm_cell(x, states=state,
	                              training=training)
	    # Convert the lstm output to a prediction.
	    prediction = self.dense(x)
	    # Add the prediction to the output.
	    predictions.append(prediction)

	  # predictions.shape => (time, batch, features)
	  predictions = tf.stack(predictions)
	  # predictions.shape => (batch, time, features)
	  predictions = tf.transpose(predictions, [1, 0, 2])
	  return predictions

trainX = np.load("trainX.npy", allow_pickle=True)
trainY = np.load("trainY.npy", allow_pickle=True)
testX = np.load("testX.npy", allow_pickle=True)
testY = np.load("testY.npy", allow_pickle=True)

trainX = tf.convert_to_tensor(trainX, dtype=tf.float32)
trainY = tf.convert_to_tensor(trainY, dtype=tf.float32)
testX = tf.convert_to_tensor(testX, dtype=tf.float32)
testY = tf.convert_to_tensor(testY, dtype=tf.float32)

feedback_model = FeedBack(units=32, out_steps=5)
prediction, state = feedback_model.warmup(trainX[0])
prediction.shape
print('Output shape (batch, time, features): ', feedback_model(trainX[0]).shape)

model = tf.keras.Sequential()
model.add(tf.keras.layers.Normalization())
model.add(tf.keras.layers.GRU(128, return_sequences=True))
model.add(tf.keras.layers.GRU(64))
model.add(tf.keras.layers.Dense(2))

model.compile(optimizer='Adam', loss='MSE', metrics = ['MeanAbsolutePercentageError'])
num_epoch = int(input("Enter number of epochs for model: "))
output = model.fit(trainX, trainY, batch_size=64, epochs=num_epoch, validation_data=(testX, testY))
model.save("trained_model")
model.summary()
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