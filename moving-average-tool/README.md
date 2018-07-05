# Moving Averages Command Line Tool

## Requirements
This tool requires that the user has Python3 installed, and was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic. It has also been tested on an Apple Macbook and worked correctly.

## Description
This tool will calculate a simple moving average from a complete node data set by averaging sensor values for time ranged windows specified by the user.

The command line tool movingAvg.py takes in a directory path and a time period. The directory path must be the full path to an unpackaged complete node data set (data sets located here: https://github.com/waggle-sensor/waggle/tree/master/data). This path must must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv. The tool will confirm that the aformentioned files exist in the passed in directory before allowing the user to begin reducing data. The time period specified determines the time range window for calculating a simple moving average (e.g. over a span of 5 mins., 1 hr., 1 day, etc.). This time ranged window will move through the data in the data.csv file. For each sensor on each node, the tool will append new sensor values to the time ranged window and throw away values outside of the time ranged window. It will constantly calculate the average of the values in this window, which becomes the simple moving average as it parses through the data. 

This tool will read the data.csv file located in the passed in directory path, parse through the large data.csv data set, and create moving averages for pieces of data (sensor values) over the time range window period given by the user. It will then create a new movingAvgData.csv file. The final output of the movingAvg.py tool will be a directory that contains the moving average data set (movingAvgData.csv) and the extra metadata files (nodes.csv, provenance.csv, README.md, and sensors.csv) from the passed in unpackaged complete node data set directory path.

**Important:** This tool has not been optimized yet and is time-window dependant; thus it will take a **very** long time (read: several days) to create moving averages for large data sets (> a few Gb) or for larger averaging time period windows (> 12h). It is **highly** recommended that a reduced data set, or an excerpt from the data.csv file, is used with this tool.

## How to Use
When typing on the terminal, the tool takes in two parameters with identifiers: input directory path (```-i, --input```) and averaging window period (```-t, --time```). 

**Input:** The path to the unpackaged complete node data set (must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv).

**Period:** The averaging window period. This parameter should be in the format ```-t #x ``` where ```#``` is an integer and ```x``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively.

**Note:** User is not allowed to enter anything less than 24 seconds because it is how often data is received and an average could not be calculated for anything lower.
**Note:** The movingAvgData.csv output file will have the headers: ```timestamp,node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_moving_average```.

Terminal command format should be like this example: ```python3 movingAvg.py -i /home/waggle-student/Downloads/AoT_Chicago.complete.2018-06-19 -t 30m```

Typing ```-h``` or ```--help``` when using this tool will pull up the help: ```python3 movingAvg.py -h```.

Errors will be specified for user error such as: not specifying the units of the period, not specifying an input file, etc.

## Step-by-Step Instructions for Creating Moving Averages
1. First follow the instructions listed at this link: ```https://github.com/waggle-sensor/waggle/tree/master/data``` to download and unpackage a complete node dataset. Place the final, entirely unpackaged directory in the desired location on your computer (make sure to complete the step that unpackages the data.csv.gz archive).
2. Clone or download the data-tools directory at this link: ```https://github.com/waggle-sensor/data-tools``` and move it to the desired location on your computer.
3. From the command line, navigate to the /data-tools/moving-average-tool directory downloaded from step 2.
4. Run the movingAvg.py tool from the command line: ```python3 movingAvg.py -i /PATH_TO_COMPLETE_NODE_DATA_SET -t #x```. Replace ```/PATH_TO_COMPLETE_NODE_DATA_SET``` with the path to the unpackaged compete node data set from step 1, ```#``` with an integer and ```x``` with one of the following characters: ```'s','m','h', or 'd'```. Remember, the directory path specified must contain the following five files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv.

## Examples

### Moving Average Over a 10 Min. Period
```
waggle-student@ermac:~/data-tools/moving-average-tool$ python3 movingAvg.py -i /home/waggle-student/Downloads/AoT_Chicago.complete.2018-06-19 -t 10m
...
2018/06/13 20:56:13,001e0610ef29,lightsense,apds_9006_020,intensity,81.983,2,40.9915
2018/06/13 20:56:13,001e0610ef29,lightsense,hih6130,humidity,92.74,2,46.37
2018/06/13 20:56:13,001e0610ef29,lightsense,hih6130,temperature,95.14,2,47.57
2018/06/13 20:56:13,001e0610ef29,lightsense,ml8511,intensity,86.28,2,43.14
2018/06/13 20:56:13,001e0610ef29,lightsense,mlx75305,intensity,1364.688,2,682.344
2018/06/13 20:56:13,001e0610ef29,lightsense,tmp421,temperature,83.15,2,41.575
2018/06/13 20:56:13,001e0610ef29,lightsense,tsl250rd,intensity,107.74,2,53.87
2018/06/13 20:56:13,001e0610ef29,lightsense,tsl260rd,intensity,114.256,2,57.128
2018/06/13 20:56:13,001e0610ef29,metsense,bmp180,pressure,1991.08,2,995.54
2018/06/13 20:56:13,001e0610ef29,metsense,bmp180,temperature,49.95,2,24.975
2018/06/13 20:56:13,001e0610ef29,metsense,hih4030,humidity,125.66,2,62.83
2018/06/13 20:56:13,001e0610ef29,metsense,htu21d,humidity,237.98,2,118.99
2018/06/13 20:56:13,001e0610ef29,metsense,htu21d,temperature,10.44,2,5.22
2018/06/13 20:56:13,001e0610ef29,metsense,metsense,id,000017e2c6a1,0,000017e2c6a1
2018/06/13 20:56:13,001e0610ef29,metsense,pr103j2,temperature,49.65,2,24.825
2018/06/13 20:56:13,001e0610ef29,metsense,spv1840lr5h_b,intensity,NA,0,NA
2018/06/13 20:56:13,001e0610ef29,metsense,tmp112,temperature,49.8,2,24.9
2018/06/13 20:56:13,001e0610ef29,metsense,tsl250rd,intensity,68.482,2,34.241
2018/06/13 20:56:13,001e0610ef29,metsense,tsys01,temperature,50.61,2,25.305
...
```
