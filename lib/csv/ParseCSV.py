import csv

with open('../../resources/employee.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # for i in range(0, len(row)):
        print(row[0] + " " + row[1] + " " + row[2])
