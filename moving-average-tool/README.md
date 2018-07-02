# Moving Averages Command Line Tool

## Requirements
This tool requires that the user has Python3 installed and the following Python modules: OrderedDict,timedelta,deque,argparse,datetime,time,csv,os, and re. OrderedDict is imported from collections, timedelta is imported from datetime, and deque is imported from collections.

This tool was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic.

## Description
The file called movingAvg.py is meant to work similarly to dataReduction.py as a command line tool that takes in a .csv file, parses the data, then outputs a .csv file. The movingAvg.py file computes a moving average for each node's sensors for a time ranged window (e.g. over a span of 5 mins., 1 hr., 1 day, etc.). The data comes from an input .csv file from the data.csv.gz data set. In the future, it is possible that this tool will be integrated with the dataReduction.py tool to make one tool.

## High Level Overview
Data is read in from the input .csv file specified in the command line. This .csv file must contain the header: 'timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf' and should come from the data.csv.gz file contained in the AoT Chicago Complete dataset @ ```https://github.com/waggle-sensor/waggle/tree/master/data```. A dictionary (sensorDict) is then created and continually updated with new sensor/timestamps within the time range window as the program runs through the input file lines. The key of this dictionary, however, differs from dataReduction.py since the key will only consist of node id, subsystem, sensor, and parameter. The value for each of these keys is a deque (queue) object that will hold the current sample of data values to be averaged and each of their timestamps. An example of the dictionary format is shown below:

```
sensorDict =
{
	'node/sensor1': deque([[val1,timestamp1],[val2,timestamp2],[val3,timestamp3]...[val(n),timestamp(n)]]), 
	'node/sensor2': deque([[val1,timestamp1],[val2,timestamp2],[val3,timestamp3]...[val(n),timestamp(n)]]),
	...
	...
}
```

Example:
```
sensorDict = 
{
	'001e0610ba46,lightsense,apds_9006_020,intensity,': deque([['1.929', '2017/03/28 20:55:19'], ['1.929', '2017/03/28 20:55:42'], ['1.849', '2017/03/28 20:56:07'], ['1.849', '2017/03/28 20:56:31'], ['1.849', '2017/03/28 20:56:55'], ['1.849', '2017/03/28 20:57:19'], ['1.849', '2017/03/28 20:57:43'], ['1.929', '2017/03/28 20:58:07'], ['1.849', '2017/03/28 20:58:33'], ['1.849', '2017/03/28 20:58:56']]),
 
	'001e0610ba46,lightsense,hih6130,humidity,': deque([['32.17', '2017/03/28 20:55:19'], ['32.18', '2017/03/28 20:55:42'], ['32.17', '2017/03/28 20:56:07'], ['32.21', '2017/03/28 20:56:31'], ['32.21', '2017/03/28 20:56:55'], ['32.22', '2017/03/28 20:57:19'], ['32.22', '2017/03/28 20:57:43'], ['32.22', '2017/03/28 20:58:07'], ['32.24', '2017/03/28 20:58:33'], ['32.25', '2017/03/28 20:58:56']]),
	...
	...
}
```
As each node/sensor queue grows with new timestamps/values, the program keeps track of the current time range period. If the values have begun to extend outside of the current time range (time range is calculated as: ```endTime = timestamp_just_queued``` and ```beginTime = timestamp_just_queued - period```), then the program will deque all values outside the time range. So, if a value is queued with a timestamp of ```2018/06/14 08:15:23``` and the period (time range) is 5 minutes, then the new end of the time range is that timestamp (```2018/06/14 08:15:23```) and the new beginning of the time range is the timestamp minus the period (```2018/06/14 08:15:23 - 00:05:00 = 2018/06/14 00:10:23```). Any timestamps in the queue that are below the new beginning of the time range are dequed and not counted in the new moving average calculation.

The program will then calculate the average of the values in the queue for the current node/sensor using the equation ```Σ(queue values)/(num. of vals in queue)```. It then writes out all the information to a line in the output file in the format:
 
```
2019/06/14 20:00:00,001e0610ba46,lightsense,apds_9006_020,intensity, 1000,10,100
```

The ranges will overlap quite a bit since it is a moving average.

**Note:** Timestamps are written out as halfway between the time range averaging window specified by the user: ```(ending_timestamp) - (period_length/2)```.

## How to Use
When typing on the terminal, the tool takes in three parameters with identifiers: input file (```-i, --input```), period (```-t, --time```), and output file (```-o, --output```). 


**Input:** Input should be a .csv file with the headers ```(timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf)```

**Period:** The period parameter should be in the format ```-t #m ``` where ```#``` is an integer and ```m``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively.

**Output:** Output should also be a .csv file which does not need to exist before executing this tool.

**Note:** User is not allowed to enter anything less than 24 seconds because it is how often data is received and an average could not be calculated for anything lower. 

Terminal command format should be like this example: 
```
waggle-student@ermac:~/summer2018/morrison/dataReductionTool$ python3 movingAvg.py -i moveAvgIn.csv -t 5h -o moveAvgOut.csv
```

Typing ```-h``` or ```--help``` when using this tool will pull up the help:
```
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ python3 movingAvg.py -h
Generating...
usage: movingAvg.py [-h] [-i INPUT] [-t PERIOD] [-o OUTPUT]

make moving averages and produce .csv file data sets from data.csv.gz

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input .csv file name
  -t PERIOD, --time PERIOD
                        moving average period. Type an int followed by
                        's','m','h',or 'd'.
  -o OUTPUT, --output OUTPUT
                        output .csv file name

```

Errors will be specified for user error such as: not specifying the units of the period, not specifying an input file, etc.

Error:
```
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ python3 movingAvg.py -i oneMillion.csv -t 5 -o moveAvgOut.csv
Generating...
Error: Time value must be an int followed by 's','m','h',or 'd'.

```

## Step-by-Step Instructions for Creating Moving Averages and Plots
1. First follow the instructions listed at this link: https://github.com/waggle-sensor/waggle/tree/master/data to download and unpackage the AoT Chicago Complete node dataset.
2. Then clone this directory: ```git clone https://github.com/waggle-sensor/summer2018.git``` into your home directory.
3. Copy the data.csv file from the downloaded complete node dataset:
  * The whole file(large, not recommended):
      * Navigate to ```/summer2018/morrison/movingAverageTool``` in the cloned directory.
      * Run ```cp /path_to_data.csv .```.
  * Part of the file (specify size, recommended):
    * Navigate to the unpackaged ```AoT_Chicago.complete.*``` directory.
    * Run ```head -n* data.csv > file_name.csv``` and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the first * lines from the data.csv file into a new file.
    * Or, run ```head -n1 data.csv > file_name.csv```, then ```tail -n* data.csv >> file_name.csv```, and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the last * lines from the data.csv file into a new file.
    * Navigate to ```/summer2018/morrison/movingAverageTool``` in the cloned directory.
    * Run ```cp /path_to_file_name.csv .```
4. Run ```python3 movingAvg.py -i file_name.csv -t #m -o output_file.csv``` replacing ```file_name``` with the name of the file you just copied, ```#``` with the moving average period, ```m``` with the units of the moving average period, and ```output_file.csv``` with the output file name (**Note:** The longer the period and the larger the input file, the longer the program will have to run).
5. Open graph.plt in the ```/summer2018/morrison/movingAverageTool``` directory and change the line ```set output...``` to the desired PDF name.
6. Still in graph.plt, change the line ```set title...``` to the desired plot title.
7. Open graph.sh in the ```/summer2018/morrison/movingAverageTool``` directory and change the first ```grep``` command for both lines to search for a specific sensor (use sensor names from the downloaded data.csv data set). Change the second ```grep``` command to change which sensor parameter is being searched for. Add (or modify if it alread exists) the third ```grep``` command to search for a certain node using the node ID, or remove it to get all nodes with that sensor. Add (or modify if it already exists) a fourth ```grep``` command to search for a specific date and/or time.
8. Continuing to edit graph.sh, change the first line's ```cat``` command file name to be the name of the file just copied (either all of or part of data.csv) and change the second ```cat``` command file name to be the output file name from running the movingAvg.py tool.
9. Run ```./graph.sh``` to generate a plot as a PDF with the file name being the name specified in step 5.

## Examples

### Moving Average Over a 10 Min. Period
```
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ python3 movingAvg.py -i smallData.csv -t 10m -o moveAvgOut.csv
Generating...
Done. Took 129.93s to complete.
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ head -n20 moveAvgOut.csv 
timestamp,node_id,subsystem,sensor,parameter,sum,count,SMA
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
```

### Moving Average Over a 1 Hr. Period
```
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ python3 movingAvg.py -i smallData.csv -t 1h -o moveAvgOut.csv
Generating...
Done. Took 186.60s to complete.
waggle-student@ermac:~/summer2018/morrison/movingAverageTool$ head -n20 moveAvgOut.csv 
timestamp,node_id,subsystem,sensor,parameter,sum,count,SMA
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
```
