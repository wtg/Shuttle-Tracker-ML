import csv
import random
import numpy as np
import tensorflow as tf
from datetime import datetime

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
def timegap(a, b):
    c = a - b
    sec_gap = c.total_seconds()
    min_gap = sec_gap / 60
    if (min_gap > 10):
        return 1
    else:
        return 0

# categorize a bus that has two data whose time gap less than 10 min to be a session
def getsession(data):
    sessions = []
    one_session = []
    prev_id = data[0][0]
    prev_time = data[0][3]
    for i in range(len(data)):
        timeGap = timegap(data[i][3], prev_time)
        if ((prev_id == data[i][0]) and (timeGap == 0)):
            one_session.append(data[i])
            prev_time = data[i][3]
        else:
            if (len(one_session) > 1):
                sessions.append(one_session)
            one_session = []
            prev_id = data[i][0]
            prev_time = data[i][3]

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
        train_len = len(i)
        x_len = (int)(train_len / 5 * 4)
        train_x.append(i[:x_len])
        train_y.append(i[x_len])
    
    for j in test:
        test_len = len(j)
        j_len = (int)(test_len / 5 * 4)
        test_x.append(j[:j_len])
        test_y.append(j[j_len:])
    
    return train_x, train_y, test_x, test_y

if __name__ == "__main__":
    # read in the data and sort by id and time
    data = readin()
    data = sorted(data, key=lambda x: (x[0], x[3]))

    # group datas into sessions of minute gap less than 10 min
    sessions = getsession(data)

    # get train and test set for sessions
    train, test = train_test(sessions)

    # get tainx trainy, and testx testy sets
    train_x, train_y, test_x, test_y = trainTest_XY(train, test)

    print(data)
    
