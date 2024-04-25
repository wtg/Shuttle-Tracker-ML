# https://stackoverflow.com/questions/67808280/tensorflow-model-with-multiple-inputs-and-single-output
import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras import Input  
from tensorflow.keras import Model 
from tensorflow.keras.layers import *
import numpy as np
print("TensorFlow version:", tf.__version__)

Input_StartTime = []
Input_DayOfWeek = []
Input_SecondsInDay = []
Input_DeltaTime = []
Output_FinalTime = []

f = open(input("Datafile: "), "r")
for line in f:
    line = line.replace("\n","")
    Input_StartTime.append(int(line.split(",")[0]))
    Input_DayOfWeek.append(int(line.split(",")[1]))
    Input_SecondsInDay.append(int(line.split(",")[2]))
    Input_DeltaTime.append(int(line.split(",")[3]))
    Output_FinalTime.append(int(line.split(",")[4]))
f.close()

Input_StartTime = np.array(Input_StartTime, dtype=np.uint32)
Input_DayOfWeek = np.array(Input_DayOfWeek, dtype=np.uint32)
Input_SecondsInDay = np.array(Input_SecondsInDay, dtype=np.uint32)
Input_DeltaTime = np.array(Input_DeltaTime, dtype=np.uint32)
Output_FinalTime = np.array(Output_FinalTime, dtype=np.uint32)

x1 = Input(shape =(1,))
x2 = Input(shape =(1,))
x3 = Input(shape =(1,))
x4 = Input(shape =(1,))

input_layer = concatenate([x1,x2,x3,x4])
hidden_layer = Dense(units=8, activation='relu')(input_layer)

prediction = Dense(1, activation='linear')(hidden_layer)
model = Model(inputs=[x1,x2,x3,x4], outputs=prediction)

model.compile(loss="mean_squared_error", optimizer='adam', metrics=['mae'])
model.fit([Input_StartTime, Input_DayOfWeek, Input_SecondsInDay, Input_DeltaTime], Output_FinalTime, epochs=300, batch_size=32, verbose=2)

# --------------------------------------------------------------------------------

# x1 = Input(shape =(1,))
# x2 = Input(shape =(1,))

# input_layer = concatenate([x1,x2])
# hidden_layer = Dense(units=4, activation='relu')(input_layer)

# prediction = Dense(1, activation='linear')(hidden_layer)
# model = Model(inputs=[x1, x2], outputs=prediction)

# model.compile(loss="mean_squared_error", optimizer='adam', metrics=['mae'])
# model.fit([inp1, inp2], tar, epochs=300, batch_size=32, verbose=2)

# --------------------------------------------------------------------------------

# model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
# model.compile(optimizer='sgd', loss='mean_squared_error')
# xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
# ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)
# model.fit(xs, ys, epochs=500)
