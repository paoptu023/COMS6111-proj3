import csv
import datetime

csvin = 'Bus_Breakdown_and_Delays.csv'
csvout = 'bus.csv'

output_file = open(csvout, 'w')
input_file = open(csvin, 'r')

writer = csv.writer(output_file)
reader = csv.reader(input_file)

for line in reader:
    if len(line[3].split()) == 3:
        date = datetime.datetime.strptime(line[3], '%m/%d/%Y %I:%M:%S %p').date()
        line[3] = datetime.datetime.strftime(date, "%H")
    elif len(line[3].split()) == 2:
        date = datetime.datetime.strptime(line[3], '%m/%d/%Y %H:%M').date()
        line[3] = datetime.datetime.strftime(date, "%H")
    else:
        line[3] = -1

    if len(line[4]) == 0:
        line[4] = 'Others'

    if len(line[6]) == 0:
        line[6] = -1
    else:
        line[6] = filter(str.isdigit, line[6])
    writer.writerows([line])

input_file.close()
output_file.close()