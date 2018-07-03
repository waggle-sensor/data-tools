# Date Range Slicing Tool

## Usage

This tool will take a project directory and a date range:

```
./slice-date-range.py project_dir start_date end_date
```

and produce a new project folder `project_dir.from-start_date-to-end_date` with
a data.csv.gz containing data only from within the specified date range.

## Example

```
$ ./slice-date-range.py ~/Downloads/Waggle_Tokyo.complete.2018-07-02/ 2018-01-01 2018-03-02
Writing data file to /Users/Sean/Downloads/Waggle_Tokyo.complete.2018-07-02.from-2018-01-01-to-2018-03-02/data.csv.gz.
Appending header.
Appending chunk for 2018-03-02.
```

```
$ ls ~/Downloads/Waggle_Tokyo.complete.2018-07-02.from-2018-01-01-to-2018-03-02/
README.md      data.csv.gz    nodes.csv      offsets.csv    provenance.csv sensors.csv
```
