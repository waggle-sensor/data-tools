#!/usr/bin/env python3
import argparse
import csv
import datetime
import gzip
import os
from shutil import copytree, ignore_patterns


def copy_project(src, dst):
    try:
        copytree(project_dir, build_dir, ignore=ignore_patterns('data.*', 'offsets.csv'))
    except FileExistsError:
        pass


def parse_date_string(s):
    try:
        return datetime.datetime.strptime(s, '%Y/%m/%d').date()
    except ValueError:
        pass

    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d').date()
    except ValueError:
        pass

    raise ValueError('Unknown date format.')


def load_offsets(filename):
    chunks = []

    with open(filename) as file:
        reader = csv.DictReader(file)

        for row in reader:
            chunks.append({
                'date': parse_date_string(row['date']),
                'offset': int(row['offset']),
                'size': int(row['size'])
            })

    return sorted(chunks, key=lambda row: row['date'])


def load_compressed_header(filename):
    with gzip.open(filename, 'rb') as file:
        return gzip.compress(file.readline())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    Splits the data.csv.gz for a project into dates/YYYY-MM-DD.csv.gz with in
    project folder.
    ''')
    parser.add_argument('project_dir')
    parser.add_argument('start_date')
    parser.add_argument('end_date')
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    start_date = parse_date_string(args.start_date)
    end_date = parse_date_string(args.end_date)
    build_dir = '{}.from-{}-to-{}'.format(project_dir, start_date, end_date)

    copy_project(project_dir, build_dir)
    chunks = load_offsets(os.path.join(project_dir, 'offsets.csv'))
    compressed_header = load_compressed_header(os.path.join(project_dir, 'data.csv.gz'))

    chunks_in_range = [c for c in chunks if start_date <= c['date'] <= end_date]

    source_data_file = os.path.join(project_dir, 'data.csv.gz')
    build_data_file = os.path.join(build_dir, 'data.csv.gz')

    print('Writing data file to {}.'.format(build_data_file))

    with open(build_data_file, 'wb') as outfile:
        print('Appending header.')
        outfile.write(compressed_header)

        with open(source_data_file, 'rb') as infile:
            for chunk in chunks_in_range:
                print('Appending chunk for {}.'.format(chunk['date']))
                infile.seek(chunk['offset'])
                data = infile.read(chunk['size'])
                outfile.write(data)
