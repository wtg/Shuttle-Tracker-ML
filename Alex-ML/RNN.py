from gc import callbacks
import numpy as np
import pandas as pd
import tensorflow as tf
import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam


df = pd.read_csv("Data_session2.csv")

df = df[:79]

latitude = df["Latitude"]
longitude = df["Longitude"]

def df_to_X_y(df, session):
    df_as_np = df.to_numpy()
    X = []
    y = []
    for i in range(len(df_as_np) - session):
        row = [[a]for a in df_as_np[i: i + session]]
        X.append(row)
        label = df_as_np[i + session]
        y.append(label)
    return np.array(X), np.array(y)

SESSION = 5
X, y = df_to_X_y(latitude, SESSION)
print(X.shape, y.shape)

X_train, y_train = X[44:1000], y[44:1000]
X_val, y_val = X[1000:1482], y[1000:1482]
X_test, y_test = X[:44], y[:44]

print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)
print(X_test.shape, y_test.shape)

model1 = Sequential()
model1.add(InputLayer((5,1)))
model1.add(LSTM(64))
model1.add(Dense(8, 'relu'))
model1.add(Dense(1, 'linear'))

model1.summary()

cp = ModelCheckpoint('model1/', save_best_only = True)
model1.compile(loss = MeanSquaredError(), optimizer = Adam(learning_rate = 0.1), metrics = [RootMeanSquaredError()])

model1.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = 10, callbacks = [cp])

X, y = df_to_X_y(longitude, SESSION)
print(X.shape, y.shape)

X_train, y_train = X[44:1000], y[44:1000]
X_val, y_val = X[1000:1482], y[1000:1482]
X_test, y_test = X[:44], y[:44]

print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)
print(X_test.shape, y_test.shape)

model2 = Sequential()
model2.add(InputLayer((5,1)))
model2.add(LSTM(64))
model2.add(Dense(8, 'relu'))
model2.add(Dense(1, 'linear'))

model2.summary()

cp = ModelCheckpoint('model1/', save_best_only = True)
model2.compile(loss = MeanSquaredError(), optimizer = Adam(learning_rate = 0.1), metrics = [RootMeanSquaredError()])

model2.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = 10, callbacks = [cp])

