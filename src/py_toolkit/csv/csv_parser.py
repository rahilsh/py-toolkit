import csv


def get_rows(file_path):
    rows = []
    with open(file_path, 'r') as file:
        for row in csv.DictReader(file):
            rows.append(row)
    return rows
