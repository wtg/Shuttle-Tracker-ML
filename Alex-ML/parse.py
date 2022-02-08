import csv


csv_file = open('Data.csv', 'r')
csv_reader = csv.reader(csv_file, delimiter = ',')

csv_list = list(csv_reader)

csv_file.close()

csv_file = open('Data_parsed.csv', 'w')
csv_file.write('ID, Latitude, Longitutde, Time, Type\n')


csv_list = csv_list[0:]

csv_list = sorted(csv_list, key = lambda x:(x[0], x[3]))


for i in csv_list:
    for j in i:
        csv_file.write(j + ' ')


    csv_file.write('\n')

csv_file.close()
