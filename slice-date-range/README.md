# Date Range Slicing Tool

## Usage

This tool will take a project directory and a date range:

```
./slice-date-range.py project_dir start_date end_date
```

and produce a new project folder `project_dir.from-start_date-to-end_date` with
a `data.csv.gz` file containing data only from within the specified date range.

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

# Split into Dates Tool

## Usage

This tool takes a project and creates a `project_dir/dates/YYYY-MM-DD.csv.gz`
file for each date-wise chunk from `data.csv.gz`.

```
$ ./split-into-dates.py project_dir
```

```
$ ls project_dir/dates
2018-06-09.csv.gz 2018-06-12.csv.gz 2018-06-15.csv.gz ...
```

It supports and optional "last n dates" argument. For example:

```
$ ./split-into-dates.py -n 7 project_dir
```

This would extract only the _last_ 7 date files.
