import csv
import pandas as pd
from datetime import datetime, timedelta


csv_file = open('Data.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter = ',')

csv_list = list(csv_reader)

csv_file.close()

csv_file = open('Data_parsed.csv', 'w')
csv_file.write('ID, Latitude, Longitude, Time, Type\n')


csv_list = csv_list[0:]

csv_list = sorted(csv_list, key = lambda x:(x[0], x[3]))
temp = ""

for i in csv_list:
    for j in i:
        temp = temp + j + ','

    result = f"{temp[0: -1]} "
    csv_file.write(result + '\n')
    temp = ""

csv_file.close()

csv_file = open('Data_parsed.csv', 'r')
data = csv.DictReader(csv_file)

data_dict = []

sessions = 0
id_check = ''
prev_time = '0000-00-00 00:00:00 +0000'

for line in data:

    if id_check != line['ID']:
        session = 0
        prev_time = line[' Time']

    if prev_time == '0000-00-00 00:00:00 +0000':
        prev_time = line[' Time']

    time_now =  pd.to_datetime(line[' Time'], utc = True)
    time_prev = pd.to_datetime(prev_time, utc = True)
    diff = (time_now - time_prev)

    if diff > timedelta(minutes = 10):
        session += 1 
        prev_time = time_now
        line[' Session'] = session
    else:
        line[' Session'] = session

    id_check = line['ID']
    data_dict.append(line)

with open('Data_session.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['ID', 'Latitude', 'Longitude', 'Time', 'Type', 'Session'])
    for i in data_dict:
       writer.writerow([i['ID'], i[' Latitude'], i[' Longitude'], i[' Time'], i[' Type'], i[' Session']])

csv_file.close()
