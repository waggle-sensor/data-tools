# Digest Plot Generation

## Overview

This tool generates plots of data over the last day, week and month, for every node. These plots are displayed in a table sorted by the ontology of the data for each node. The tables contain links to each plot that exists. Not every node has data for every ontology, so those rows are unlinked. The plots can be updated daily.

## Requirements  

This tool depends on **python3**, **numpy** and **pandas** packages for python3, as well as **gnuplot**. Please make sure they are installed in the system where they are intended to be used.  
The bash shell scripts this tool uses require a Linux or Mac OS X environment to run.  
The project directory used as input must have the following files:
* `data.csv.gz`
* `nodes.csv`
* `sensors.csv`
* `offsets.csv`  

**Note:** this tool specifically requires `data.csv.gz`, not `data.csv`

## How to Use

To run the scripts, use the command line to navigate to the `digest-plot` directory within the repository.  

To retrieve data run `./stage_project.sh project_id`  
To generate the plots run `./create_project_graphs.sh project_directory_path`  
To generate the tables run `gen_tables.py`


### Example
```
$ ./stage_project.sh AoT_Portland
--2018-07-10 11:21:56--  http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Portland.complete.latest.tar
Resolving www.mcs.anl.gov (www.mcs.anl.gov)... 140.221.6.95
Connecting to www.mcs.anl.gov (www.mcs.anl.gov)|140.221.6.95|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 83896320 (80M) [application/x-tar]
Saving to: ‘./scratch/AoT_Portland.complete.latest.tar.1’

AoT_Portland.complete.latest.tar.1                         100%[========================================================================================================================================>]  80.01M  11.2MB/s    in 7.2s    

2018-07-10 11:22:03 (11.2 MB/s) - ‘./scratch/AoT_Portland.complete.latest.tar.1’ saved [83896320/83896320]

File Downloaded
File Untared
```
```
$ ./create_project_graphs.sh scratch/AoT_Portland.complete.2018-07-09/
Writing data file to /home/waggle-student/Documents/repos/data-tools/digest-plot/scratch/AoT_Portland.complete.2018-07-09.from-2018-07-09-to-2018-07-09/data.csv.gz.
Appending header.
Appending chunk for 2018-07-09.
Extracting node data for 2018-07-09.
Writing data file to /home/waggle-student/Documents/repos/data-tools/digest-plot/scratch/AoT_Portland.complete.2018-07-09.from-2018-07-08-to-2018-07-08/data.csv.gz.
Appending header.
Appending chunk for 2018-07-08.
Extracting node data for 2018-07-08.
...
Writing data file to /home/waggle-student/Documents/repos/data-tools/digest-plot/scratch/AoT_Portland.complete.2018-07-09.from-2018-06-11-to-2018-06-11/data.csv.gz.
Appending header.
Extracting node data for 2018-06-11.
Writing data file to /home/waggle-student/Documents/repos/data-tools/digest-plot/scratch/AoT_Portland.complete.2018-07-09.from-2018-06-10-to-2018-06-10/data.csv.gz.
Appending header.
Extracting node data for 2018-06-10.
Extracting 001e0610e545/2018-06-14...
Extracting 001e0610e545/2018-06-10...
Extracting 001e0610e545/2018-06-13...
...
Extracting 001e06113d6d/2018-07-01...
Extracting 001e06113d6d/2018-07-02...
Extracting 001e06113d6d/2018-06-25...
Combining data for 001e0610e545 for the last day...
Combining data for 001e0610e545 for the last week...
Combining data for 001e0610e545 for the last month...
Combining data for 001e06113a07 for the last day...
Combining data for 001e06113a07 for the last week...
Combining data for 001e06113a07 for the last month...
Combining data for 001e06113d6d for the last day...
Combining data for 001e06113d6d for the last week...
Combining data for 001e06113d6d for the last month...
Plotting 001e06113a07 week /sensing/air_quality
Plotting 001e06113a07 week /sensing/meteorology/humidity
...
Plotting 001e06113a07 week /system/other/temperature
Plotting 001e06113a07 week /system/other/sampling_period
Plotting 001e06113a07 month /sensing/air_quality
Plotting 001e06113a07 month /sensing/meteorology/humidity
...
Plotting 001e06113a07 month /system/other/temperature
Plotting 001e06113a07 month /system/other/sampling_period

```




* `project_id` is the id of the project you want to plot data from substituting underscores for spaces
* eg. `./stage_project AoT_Chicago`, `./stage_project AoT_Portland`, `./stage_project NUCWR-MUGS`  

* `project_directory` is the directory created by `stage_project.sh`
* eg. `./create_project_graphs.sh AoT_Chicago.complete.2018-07-09`, `./create_project_graphs.sh AoT_Portland.complete.2018-06-24`
* The directory will always be the project idea used previously, followed by complete, followed by the date the dataset is from.

## Documentation

### Data Retrieval

`stage_project.sh project_id` downloads and untars a project based on its id.  

`project_id` is the id of the project to download. A list of datasets for different projects is available at http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php.

### Data Extraction and Plot Generation

`create_project_graphs.sh project_directory_path` calls multiple other scripts in order to extract the data into plottable datasets and generate plots using those datasets.  

`project_directory_path` is the path to the directory created by `stage_project.sh`, inside the `scratch` directory, which contains `data.csv.gz`, `nodes.csv`, `sensors.csv`, `offsets.csv`, `provenance.csv`, and `README.md`.  

Given a valid project directory, the `slice-date-range` tool is used to cut `data.csv.gz` into daily slices and uncompress the resulting files. Then `extract_nodes.py` is used to get the data for each node from each day. Then `gen_digest_plots.py` extracts the rest of the data for each ontology into a plottable dataset and generates plots for all of the data that exists for each node.



The data is obtained from a complete data set at http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php. The data is then split into daily chunks using the `slice-date-range` tool which can also be found in this repository. Then data for each node is extracted from the daily chunks, and finally the data for each ontology is extracted. The data is then combined into 1 day, 7 day and 30 day datasets suitable for plotting.

## Plot Generation

Plots are generated for each of the 3 time periods, day, week and month every time the script is executed. Plot generation generally consists of setting up parameters to be written to `graph.plt` to be plotted by gnuplot.

## Table Generation

Tables for each node are generated based on the ontologies present in `sensors.csv` from requested dataset. For each ontology, if a corresponding plot exists, then a link to that plot will be in the table.
