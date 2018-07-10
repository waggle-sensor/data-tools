# Digest Plot Generation

## Overview

This tool generates plots of data over the last day, week and month, for every node. These plots are displayed in a table sorted by the ontology of the data for each node. The tables contain links to each plot that exists. Not every node has data for every ontology, so those rows are unlinked. The plots can be updated daily.

## Requirements  

This tool depends on **python3**, **numpy** and **pandas** packages for python3, as well as **gnuplot**. Please make sure they are installed in the system where they are intended to be used.  
The bash shell scripts this tool uses require a Linux or Mac OS X environment to run.  
Plotting also requires that the 

This tool relies on `plotting utilities.py`, `extract.sh` and `cut.sh` in the parent directory. It also requires the pandas and numpy packages for python.

To generate the plots run `gen_waggle_plot.py`  
To generate the tables run `gen_tables.py`

## Data Handling

The data is obtained from the complete data set at http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.latest.tar. Then the data for each ontology/parameter is extracted from the dataset for each day. Finally, the datasets for each ontology/parameter for each day are combined using data from the last 1, 7 or 30 days. This results in the final data sets used for plotting.  

If data is already downloaded on the machine, and the script is run to update the plots the next day, the data from 31 days ago will be deleted. Only the data from the most recent day will be downloaded and extracted. Then all of the data will be recombined. If the script is run again on the same day, all data handling steps are skipped.

## Plot Generation

Plots are generated for each of the 3 time periods, day, week and month every time the script is executed. Plot generation generally consists of setting up parameters to be written to `graph.plt` to be plotted by gnuplot.

## Table Generation

Tables for each node are generated based on the ontologies present in `sensors.csv` from https://github.com/waggle-sensor/beehive-server/blob/newformat/publishing-tools/projects/AoT_Chicago.complete/sensors.csv. For each ontology, if a corresponding plot exists, then a link to that plot will be in the table.