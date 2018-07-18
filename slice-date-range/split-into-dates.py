#!/usr/bin/env python3
import argparse
import csv
import gzip
import os

parser = argparse.ArgumentParser(description='''
Splits the data.csv.gz for a project into dates/YYYY-MM-DD.csv.gz with in
project folder.
''')
parser.add_argument('-n', type=int, help='Split last n dates.')
parser.add_argument('project_dir')
args = parser.parse_args()

os.chdir(args.project_dir)

# read chunks files
chunks = []

with open('offsets.csv') as file:
    reader = csv.DictReader(file)

    for row in reader:
        chunks.append({
            'date': row['date'],
            'offset': int(row['offset']),
            'size': int(row['size'])
        })

if args.n is not None:
    chunks = chunks[-args.n:]

# get compressed header. will be inserted at start of each date file.
with gzip.open('data.csv.gz', 'rb') as file:
    header = file.readline()

compressed_header = gzip.compress(header)

# export date files to dates/YYYY-MM-DD.csv.gz
os.makedirs('dates', exist_ok=True)

with open('data.csv.gz', 'rb') as file:
    for chunk in chunks:
        file.seek(chunk['offset'])
        data = file.read(chunk['size'])

        with open(os.path.join('dates', chunk['date'] + '.csv.gz'), 'wb') as outfile:
            outfile.write(compressed_header)
            outfile.write(data)
