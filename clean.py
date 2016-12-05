import csv, re
import datetime

csvin = 'Bus_Breakdown_and_Delays.csv'
csvout = 'INTEGRATED-DATASET.csv'

output_file = open(csvout, 'w')
input_file = open(csvin, 'r')

writer = csv.writer(output_file)
reader = csv.reader(input_file)

headers = next(reader, None)
writer.writerow(headers)

for line in reader:
    d = line[2]
    if len(d.split()) == 3:
        date = datetime.datetime.strptime(d, '%m/%d/%Y %I:%M:%S %p')
        line[2] = datetime.datetime.strftime(date, '%H') + ' O\'Clock'
    elif len(d.split()) == 2:
        date = datetime.datetime.strptime(d, '%m/%d/%Y %H:%M')
        line[2] = datetime.datetime.strftime(date, '%H') + ' O\'Clock'
    elif len(d.split()) == 0:
        line[2] = -1

    if len(line[3]) == 0:
        line[3] = 'Others'

    if len(line[5]) == 0:
        line[5] = -1
    elif len(line[5]) != 0:
        non_decimal = re.compile(r'[^\d-]+')
        time = non_decimal.sub('', line[5])
        if 'h' in line[5].lower():
            line[5] = time + ' HR'
        else:
            line[5] = time + ' MIN'

    if '(' in line[4]:
        ind = line[4].index('(')
        line[4] = line[4][:ind]
    writer.writerows([line])

input_file.close()
output_file.close()
