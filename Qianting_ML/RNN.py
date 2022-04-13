import csv
import random
from sqlite3 import DatabaseError
import numpy as np
from requests import Session
import tensorflow as tf
from datetime import datetime
from tensorflow import keras
from tensorflow.keras import layers

# return datetime to string
def convert_2_string(time_Var):
    result = time_Var.strftime("%Y-%m-%d %H:%M:%S %z")
    return result

# return a combined string
def combine(x):
    temp = x[0]
    length = len(temp)
    result = temp.ljust(5 - length, ' ')

    temp = x[1]
    length = len(temp)
    result += temp.ljust(50 - length, ' ')

    temp = x[2]
    length = len(temp)
    result += temp.ljust(50 - length, ' ')

    temp = convert_2_string(x[3])
    length = len(temp)
    result += temp.ljust(52 - length, ' ')

    temp = x[4]
    length = len(temp)
    result += temp.ljust(14 - length, ' ')
    
    
    temp = str(x[5])
    length = len(temp)
    result += temp.ljust(5 - length, ' ')

    return result

#output
def output(sorted_data):
    temp = "id logitude                                   latitude                                   time                                 type  index"
    print(temp)

    index = 0
    prev_name = sorted_data[0][0]
    prev_index = sorted_data[0][5]
    for x in sorted_data:
        current_index = x[5]
        if (x[5] > prev_index):
            prev_index = x[5]
            index += 1
        x[5] = index
        str_var = combine(x)
        print(str_var)    

# convert time into standard ISO 8601 format
def convert_2_dateTime(string):
    count = 0
    temp = ""
    temp += string[:10]
    temp += 'T'
    temp += string[11:19]
    temp += ".000000"
    temp += string[20:23]
    temp += ':'
    temp += string[23:]

    result = datetime.fromisoformat(temp)

    return result

# read in cvs
def readin():
    # saving it into an array
    data = []
    file_name = 'Data.csv'
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader: 
            data.append(row)

    # convert time into datetime & set start time
    for line in data:
        line[0] = float(line[0])
        line[1] = float(line[1])
        line[2] = float(line[2])
        line[3] = convert_2_dateTime(line[3])  
        line.pop()
    return data

# return 1 if time gap > 10 min, else return 0;
def isBiggerThan10MIn(a, b):
    c = a - b
    sec_gap = c.total_seconds()
    min_gap = sec_gap / 60
    if (min_gap > 10):
        return 1
    else:
        return 0

# return timegap in minutes
def timegap(a, b):
    c = a - b
    sec_gap = c.total_seconds()
    min_gap = sec_gap / 60
    return min_gap

# categorize a bus that has two data whose time gap less than 10 min to be a session
def getsession(data):
    sessions = []
    one_session = []
    prev_id = data[0][0]
    prev_time = data[0][3]
    for i in range(len(data)):
        timeGap = isBiggerThan10MIn(data[i][3], prev_time)
        if ((prev_id == data[i][0]) and (timeGap == 0)):
            one_session.append(data[i][1:])
            #one_session.append(data[i])
            prev_time = data[i][3]
        else:
            if (len(one_session) >= 2):
                sessions.append(one_session)
            one_session = []
            #one_session.append(data[i])
            one_session.append(data[i][1:])
            prev_id = data[i][0]
            prev_time = data[i][3]

    return sessions

# convert datetime in each data into float (the time gap between start time and current time)
def datetime2Float(sessions):
    for data in sessions:
        #data = sorted(data, key=lambda x: (x[2]))

        #prev_t = data[0][3]
        prev_t = data[0][2]

        for per_data in data:
            #timeGap = timegap(per_data[3], prev_t)
            #prev_t = per_data[3]
            #per_data[3] = timeGap
            timeGap = timegap(per_data[2], prev_t)
            prev_t = per_data[2]
            per_data[2] = timeGap

    return sessions

# catagorize train and test set
def train_test(sessions):
    train = []
    test = []
    session_len = len(sessions)
    train_num = (int)(session_len / 5 * 4)
    while (len(train) != train_num):
        index = random.randint(0, session_len - 1)
        if sessions[index] not in train:
            train.append(sessions[index])

    for x in sessions:
        if x not in train:
            test.append(x)

    return train, test

# classify train and test into trainx,trainym testx, testy
def trainTest_XY(train, test):
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    for i in train:
        train_len = len(i) - 1
        train_x.append(i[:train_len])
        train_y.append(i[train_len])

    for j in test:
        test_len = len(j) - 1
        test_x.append(j[:test_len])
        test_y.append(j[test_len])

    return train_x, train_y, test_x, test_y

# convert trainx trainy testx testy into tensor
def convertArray(trainx, trainy, testx, testy):
    TrainX = np.array(trainx, dtype=object)
    TrainX = tf.ragged.constant(TrainX)

    TrainY = tf.convert_to_tensor(trainy, dtype='float32')

    TstX = np.array(testx, dtype=object)
    TstX = tf.ragged.constant(TstX)

    TstY = tf.convert_to_tensor(test_y, dtype='float32')

    return TrainX, TrainY, TstX, TstY


if __name__ == "__main__":
    # read in the data and sort by id and time
    data = readin()
    data = sorted(data, key=lambda x: (x[0], x[3]))

    # remove id, and group datas into sessions of minute gap less than 10 min
    sessions = getsession(data)

    # convert datetime into float by calculating the timegap between the starttime and the current time
    sessions = datetime2Float(sessions)

    print("finished sessions!!!!!!!")

    # get train and test set for sessions
    train, test = train_test(sessions)

    print("finishd train, test!!!!!!!!!!!!!!!!!")

    # get tainx trainy, and testx testy sets
    train_x, train_y, test_x, test_y = trainTest_XY(train, test)

    print("finished trainx, trainy, testx, testy!!!!!!!!!!!!")
    
    # convert trainx, trainy, testx, testy into tensor
    TrainX, TrainY, TstX, TstY = convertArray(train_x, train_y, test_x, test_y)

    print("finished padded")

    # pad the ragged data into matrixes
    padded_trainX = TrainX.to_tensor(0.)
    padded_TstX = TstX.to_tensor(0.)

   
    # build models
    inputs = tf.keras.Input((None, 3))
    #x1 = tf.keras.layers.Dense(8)(inputs)
    #x2 = tf.keras.layers.Dropout(0.02)(x1) 
    #x2 = tf.keras.layers.Dense(3)(x1)
    #x3 = tf.keras.layers.BatchNormalization()(x2)
    x2 = tf.keras.layers.LSTM(64, return_sequences=True)(inputs)
    x4 = tf.keras.layers.LSTM(64, return_sequences=False)(x2)
    #x1 = tf.keras.layers.SimpleRNN(64, dropout=0.5, activation='linear')(inputs)
    #outputs = tf.keras.layers.Dense(3)(x1)
    #x6 = tf.keras.layers.LayerNormalization()(x4)
    #x6 = tf.keras.layers.Dense(8)(x4)
    #x8 = tf.keras.layers.Dropout(0.2)(x4) 
    outputs = tf.keras.layers.Dense(3)(x4)
    model = tf.keras.Model(inputs=inputs,outputs=outputs)

    model.compile(loss = tf.keras.losses.MeanSquaredError(), optimizer = tf.keras.optimizers.Adam(learning_rate = 0.003), metrics=['acc','mae'])
    #model.compile(loss = tf.keras.losses.MeanAbsolutePercentageError(), optimizer = tf.keras.optimizers.Adam(learning_rate = 0.003), metrics=['mse','mae'])

    cp = tf.keras.callbacks.ModelCheckpoint("best_model", monitor = 'val_loss', save_best_only=True, save_freq='epoch')
    history = model.fit(padded_trainX, TrainY, batch_size=8, epochs=30, callbacks = [cp], validation_split=0.1)
    #history = model.fit(padded_trainX, TrainY, epochs=30, callbacks = [cp], validation_split=0.1)
    model.summary()

    result = model.evaluate(TstX, TstY, callbacks = [cp])
    #result = model.evaluate(TstX, TstY)
    print("test loss, test acc:", result)

    predictions = model.predict(TstX[10:20])
    print("predictions shape:", predictions.shape, ", result: \n", predictions)
    print("\n__\nanser:\n\n\n\n", TstY[10:20])
    print("\n__\ntestx:\n", TstX[10:20])