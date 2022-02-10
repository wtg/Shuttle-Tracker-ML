import csv
from datetime import datetime

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

# return group index
def index(a, b):
    c = a - b
    temp = c.total_seconds()
    total_min = temp / 60

    result = total_min / 10
    result = int(result)
    
    left = total_min % 10

    if ((a != b) and (left == 0)):
        return (result + 1)
    else:
        return result

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

if __name__ == "__main__":
    # saving it into an array
    data = []
    file_name = 'Data.csv'
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader: 
            data.append(row)

    # convert time into datetime & set start time
    for line in data:
        line[3] = convert_2_dateTime(line[3])
    
    # sort by id and time
    sorted_data = sorted(data, key=lambda x: (x[0], x[3]))
    start_time = data[0][3]

    # append group id in each row
    for x in sorted_data:
        group_id = index(x[3], start_time)
        x.append(group_id)

    # sort by id and time and group index
    sorted_data = sorted(data, key=lambda x: (x[5], x[0], x[3]))
    start_time = data[0][3]
    
    temp = "id logitude                                   latitude                                   time                                 type  index"
    print(temp)

    index = 0
    prev_index = sorted_data[0][5]
    for x in sorted_data:
        current_index = x[5]
        if (x[5] > prev_index):
            prev_index = x[5]
            index += 1
        x[5] = index
        str_var = combine(x)
        print(str_var)