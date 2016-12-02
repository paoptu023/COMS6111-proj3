import csv, re
import datetime

csvin = 'Bus_Breakdown_and_Delays.csv'
csvout = 'bus.csv'

output_file = open(csvout, 'w')
input_file = open(csvin, 'r')

writer = csv.writer(output_file)
reader = csv.reader(input_file)

headers = next(reader, None)
writer.writerow(headers)

for line in reader:
    d = line[3]
    if len(line[3].split()) == 3:
        date = datetime.datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p')
        line[3] = datetime.datetime.strftime(date, '%H') + ' O\'Clock'
    elif len(line[3].split()) == 2:
        date = datetime.datetime.strptime(d, '%m/%d/%Y %H:%M')
        line[3] = datetime.datetime.strftime(date, '%H') + ' O\'Clock'
    elif len(line[3].split()) == 0:
        line[3] = -1

    if len(line[4]) == 0:
        line[4] = 'Others'

    if len(line[6]) == 0:
        line[6] = -1
    elif len(line[6]) != 0:
        non_decimal = re.compile(r'[^\d-]+')
        time = non_decimal.sub('', line[6])
        if 'h' in line[6].lower():
            line[6] = time + ' HR'
        else:
            line[6] = time + ' MIN'

    if '(' in line[5]:
        ind = line[5].index('(')
        line[5] = line[5][:ind]
    writer.writerows([line])

input_file.close()
output_file.close()
