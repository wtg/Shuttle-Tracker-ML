import csv
import pandas as pd
from datetime import datetime


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

data_dict = {'ID':[], 'Latitude':[], 'Longitude':[], 'Time':[], 'Type':[]}

for line in data:
    data_dict['ID'].append(line['ID'])
    data_dict['Latitude'].append(line[' Latitude'])
    data_dict['Longitude'].append(line[' Longitude'])
    data_dict['Time'].append(line[' Time'][:20])
    data_dict['Type'].append(line[' Type'])


df = pd.DataFrame(data_dict, columns = ['ID', 'Latitude', 'Longitude', 'Time', 'Type'])
df['Time'] =  pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S')

df['Session'] = (df.groupby('ID')['Time'].transform(lambda x: x.diff().dt.seconds.gt(300).cumsum()))

csv_write = open('Data_session.csv', 'w')

df.to_csv('Data_session.csv', sep = ',',encoding='utf-8' )

print(df)
