# https://www.tensorflow.org/guide/keras/functional_api

import tensorflow as tf
import numpy as np

AllInputs1 = []
AllInputs2 = []
AllOutputs1 = []
AllOutputs2 = []

# Grab info from file
FileName = input("Data File Name: ")
totalLines = 0
with open(FileName, 'r') as file:
    totalLines = sum(1 for _ in file)
with open(FileName, 'r') as fileRead:
    lineCur = 0
    percent = 0
    for line in fileRead:
        lineCur += 1
        if (lineCur % int(totalLines / 10) == 0):
            percent += 10
            print(str(percent) + "% done reading input file")

        splitUp = line.split(",")
        AllInputs1.append(splitUp[1])
        AllInputs2.append(splitUp[2])
        AllOutputs1.append(splitUp[3])
        AllOutputs2.append(splitUp[4])

AllInputs1 = np.array(AllInputs1, dtype=np.int64)
AllInputs2 = np.array(AllInputs2, dtype=np.int64)
AllOutputs1 = np.array(AllOutputs1, dtype=np.int64)
AllOutputs2 = np.array(AllOutputs2, dtype=np.int64)

input1 = tf.keras.layers.Input(shape=(1,), name='PositionStart')
input2 = tf.keras.layers.Input(shape=(1,), name='Time')
concatenated_inputs = tf.keras.layers.Concatenate()([input1, input2])
hidden1 = tf.keras.layers.Dense(32, activation='relu')(concatenated_inputs)
hidden2 = tf.keras.layers.Dense(16, activation='relu')(hidden1)
output1 = tf.keras.layers.Dense(1, name='PositionEnd')(hidden2)
output2 = tf.keras.layers.Dense(1, name='TimeUntil')(hidden2)
model = tf.keras.models.Model(inputs=[input1, input2], outputs=[output1, output2])
model.compile(optimizer='adam', loss='mse')
model.summary()

model.fit(x=[AllInputs1, AllInputs2], y=[AllOutputs1, AllOutputs2], epochs=1000, verbose=1)
# end: 1408/1408 [==============================] - 4s 3ms/step - loss: 2600360960.0000 - PositionEnd_loss: 166005.5000 - TimeUntil_loss: 2600180224.0000