import csv


def get_rows(file_path):
    rows = []
    for row in csv.DictReader(open(file_path, 'r')):
        rows.append(row)
    return rows