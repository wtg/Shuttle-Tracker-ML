from gc import callbacks
from tabnanny import verbose
import numpy as np
import pandas as pd
import tensorflow as tf
import numpy as np, pandas as pd, matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.losses import MeanAbsolutePercentageError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam


df = pd.read_csv("Data_session2.csv")



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

print("LATITUDE MODEL \n")

SESSION = 5
X, y = df_to_X_y(latitude, 5)
print(X.shape, y.shape)

X_train, y_train = X[:2000], y[:2000]
X_val, y_val = X[2000:4000], y[2000:4000]
X_test, y_test = X[4000:], y[4000:]

print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)
print(X_test.shape, y_test.shape)

model1 = Sequential()
model1.add(InputLayer((5,1)))
model1.add(LSTM(100,recurrent_dropout= 0.1))
model1.add(Dense(5, activation = 'relu'))
model1.add(Dense(1, activation = 'linear'))

model1.summary()

cp = ModelCheckpoint('model1/', save_best_only = True)
model1.compile(loss = MeanAbsolutePercentageError(), optimizer = Adam(learning_rate = 0.001),metrics = ['accuracy'])

model1.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = 10, callbacks = [cp])

score = model1.evaluate(X_test, y_test)

print('test loss', score)
#print('accuracy', score[1])

# print("LONGITUDE MODEL \n")

# X, y = df_to_X_y(longitude, SESSION)
# print(X.shape, y.shape)

# X_train, y_train = X[:2000], y[:2000]
# X_val, y_val = X[2000:4000], y[2000:4000]
# X_test, y_test = X[4000:], y[4000:]

# print(X_train.shape, y_train.shape)
# print(X_val.shape, y_val.shape)
# print(X_test.shape, y_test.shape)

# model2 = Sequential()
# model2.add(InputLayer((5,1)))
# model2.add(LSTM(100))
# model2.add(Dense(8, 'relu'))
# model2.add(Dense(1, 'linear'))

# model2.summary()

# cp = ModelCheckpoint('model1/', save_best_only = True)
# model2.compile(loss = MeanSquaredError(), optimizer = Adam(learning_rate = 0.01), metrics = [RootMeanSquaredError()])

# model2.fit(X_train, y_train, validation_data = (X_val, y_val), epochs = 5, callbacks = [cp])


# print('test loss', model2.evaluate(X_test, y_test, verbose = 0)[0])
# print('accuracy', model2.evaluate(X_test, y_test, verbose = 0)[1])
