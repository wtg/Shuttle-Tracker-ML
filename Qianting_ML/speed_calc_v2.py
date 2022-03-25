import csv
import random
import numpy as np
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
            one_session.append(data[i])
            prev_time = data[i][3]
        else:
            if (len(one_session) >= 2):
                sessions.append(one_session)
            one_session = []
            one_session.append(data[i])
            prev_id = data[i][0]
            prev_time = data[i][3]

    return sessions

# convert datetime in each data into float (the time gap between start time and current time)
def datetime2Float(sessions):
    start_t = sessions[0][0][3]
    for data in sessions:
        for per_data in data:
            timeGap = timegap(per_data[3], start_t)
            per_data[3] = timeGap
    return sessions
    
# catagorize train and test set
def train_test(sessions):
    train = []
    test = []
    session_len = len(sessions)
    train_num = (int)(session_len / 5 * 4)
    while (len(train) != train_num):
        index = random.randint(0, train_num)
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

    # group datas into sessions of minute gap less than 10 min
    sessions = getsession(data)

    # convert datetime into float by calculating the timegap between the starttime and the current time
    sessions = datetime2Float(sessions)

    # get train and test set for sessions
    train, test = train_test(sessions)

    # get tainx trainy, and testx testy sets
    train_x, train_y, test_x, test_y = trainTest_XY(train, test)

    # convert trainx, trainy, testx, testy into tensor
    TrainX, TrainY, TstX, TstY = convertArray(train_x, train_y, test_x, test_y)

    # pad the ragged data into matrixes
    padded_trainX = TrainX.to_tensor(0.)
    padded_TstX = TstX.to_tensor(0.)

    print("shape is ", padded_trainX.shape)
    print("shape for test is ", padded_TstX.shape)
    print(TrainY)

    # build models
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.InputLayer((None, 4)))
    model.add(layers.SimpleRNN(512, return_sequences = True, activation='relu'))
    model.add(layers.SimpleRNN(512, activation='relu'))
    model.add(layers.Dense(4))
    model.compile(loss = tf.keras.losses.MeanSquaredError(), optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001), metrics=['accuracy'])

    model.fit(padded_trainX, TrainY, batch_size=10, epochs=10)
    model.summary()


