# Data Reduction Command Line Tool

## Requirements
This tool requires that the user has Python3 installed and the following Python modules: OrderedDict, timedelta, timedelta, argparse, datetime, time, csv, io, os, and re. OrderedDict is imported from collections and timedelta is importedfrom datetime.

This was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic.

## Description

There are two files located in this directory that can be used to reduce data: dataReduction.py and dataReduction.sh. The dataReduction.py file is a python script where the user can manually change the arguments to  reduce data, and reduce data only. The dataReduction.sh file is a BASH script that automates the data reduction process by already specifying the arguments for the user. It also automatically bundles the reduced data set with metadata files to create a new archive.

### dataReduction.py: Data Reduction Script
The file dataReduction.py takes in an input .csv file, a time period, and an output .csv file. The input .csv file must contain the header: 'timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf' and should come from the data.csv.gz file contained in the AoT Chicago Complete dataset @ ```https://github.com/waggle-sensor/waggle/tree/master/data```. It then reads the input .csv file, parses through the large csv data set, and reduces the amount of data by averaging/combining pieces of data (sensor values) over a certain time period given by the user. Then it writes out a new .csv file. Timestamps are written out as halfway between the interval specified by the user (see **High Level Overview** for examples). This script functions as a stand alone command line tool.

### dataReduction.sh: Data Reduction and Archival Script
The file dataReduction.sh is a BASH script that takes in a single parameter (the same as the -t parameter for dataReduction.py without the -t specifier): ```#m ``` where ```#``` is an integer and ```m``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively. This script runs the dataReduction.py tool, then creates a .tar archive of the reduced data and the metadata files included with the downloaded full data set.

## High Level Overview of dataReduction.py
The file .csv input is given as: 
```
(timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf)
```

Create dictionary keys using reduced timestamps from user input and editing out sensor values:

```
(reduced_timestamp, node_id, subsystem, sensor, parameter)
```

Reduced timestamp examples:

hourly: ```2018/05/01 11:20:39``` would reduce and be output as ```2018/05/01 11:30:00``` since it is between the 11th and 12th hours of that day.

daily: ```2018/05/01 11:20:39``` would reduce and be output as ```2018/05/01 12:00:00``` since the timestamp occurs on that day.

Accumulation is done roughly as:

```(count, sum) = aggregates[reduced_key]``` 
```aggregates[reduced_key] = (count + 1, sum + value)```

Rows of the output .csv file are in the form: timestamp,node_id,subsystem,sensor,parameter,sum,count,average. But they are stored as key-value pairs: 

```outputDictionary[reduced_key] = (count, sum, average)```


## How to Use dataReduction.py

When typing on the terminal, the tool takes in three required parameters with identifiers and one optional parameter with an identifier: input file (```-i, --input```), time period (```-t, --time```), output file (```-o, --output```), and verbose option for number of lines parsed (```-v, --verbose```).

**Input:** Input should be a .csv file with the headers ```(timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf)```

**Period:** The period parameter should be in the format ```-t #m ``` where ```#``` is an integer and ```m``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively.

**Output:** Output should also be a .csv file which does not need to exist before executing this tool. The output .csv file of this tool will have the headers: ```timestamp,node_id,subsystem,sensor,parameter,sum,count,average``` all the time. If there are more than a certain number of values (1000 right now) in any of the averaging periods, the tool will output the .csv file with the headers: ```timestamp,node_id,subsystem,sensor,parameter,sum,count,average,min,max```. It includes a minimum and maximum value per averaging period that is useful when graphing or analyzing the output data.

**Verbose:** Optional parameter. Specifying the verbose option with an integer will print out the number of lines parsed for every increment of the integer passed in (e.g. if user enters 1000, every 1000 lines the program will print the number of lines - 1000, 2000, 3000...)

**Note:** User is not allowed to enter anything less than 24 seconds because it is how often data is received and an average could not be calculated for anything lower. 

Terminal command format should be like these examples: ```python3 dataReduction.py -i oneMillion.csv -t 12h -o newOutput.csv``` or ```python3 dataReduction.py -i oneMillion.csv -t 12h -o newOutput.csv -v 1000```

Typing ```-h``` or ```--help``` when using this tool will pull up the help:
```
waggle-student@ermac:~/summer2018/morrison/dataReductionTool$ time python3 dataReduction.py -h
Generating...
usage: dataReduction.py [-h] [-i INPUT] [-t PERIOD] [-o OUTPUT] [-v NUMLINES]

average and reduce .csv file data sets from data.csv.gz

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input .csv file name.
  -t PERIOD, --time PERIOD
                        Rows condense over this amt of time. Type an int
                        followed by 's','m','h',or 'd'.
  -o OUTPUT, --output OUTPUT
                        Output .csv file name.
  -v NUMLINES, --verbose NUMLINES
                        Type an int. Prints # of lines parsed for every
                        increment of entered int.
```

Errors will be specified for user error such as: not all of the parameters being filled in when using the tool, not specifying an input file, or specifying an input or output file that is not .csv format

Error:
```
waggle-student@ermac:~/summer2018/morrison/dataReductionTool$ python3 dataReduction.py -i oneMillion.csv -t 30s -o avgOut
Generating...
Error: Output file must be .csv.
```

## Step-by-Step Instructions

### dataReduction.py: Data Reduction Script (Manual) and Plotting
1. First follow the instructions listed at this link: https://github.com/waggle-sensor/waggle/tree/master/data to download and unpackage the AoT Chicago Complete node dataset.
2. Then clone this directory: ```git clone https://github.com/waggle-sensor/summer2018.git``` into your home directory.
3. Copy the data.csv file from the downloaded complete node dataset:
  * The whole file(large, not recommended):
      * Navigate to ```/summer2018/morrison/dataReductionTool``` in the cloned directory.
      * Run ```cp /path_to_data.csv .```.
  * Part of the file (specify size, recommended):
    * Navigate to the unpackaged ```AoT_Chicago.complete.*``` directory.
    * Run ```head -n* data.csv > file_name.csv``` and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the first * lines from the data.csv file into a new file.
    * Or, run ```head -n1 data.csv > file_name.csv```, then ```tail -n* data.csv >> file_name.csv```, and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the last * lines from the data.csv file into a new file.
    * Navigate to ```/summer2018/morrison/dataReductionTool``` in the cloned directory.
    * Run ```cp /path_to_file_name.csv .```
4. Run ```python3 dataReduction.py -i file_name.csv -t #m -o output_file.csv``` replacing ```file_name``` with the name of the file you just copied, ```#``` with the time period, ```m``` with the units of the time period, and ```output_file.csv``` with the output file name. Specify ```-v``` with an integer to see the number of lines being parsed.
5. Open graph.plt in the ```/summer2018/morrison/dataReductionTool``` directory and change the line ```set output...``` to the desired PDF name.
6. Still in graph.plt, change the line ```set title...``` to the desired plot title.
7. Open graph.sh in the ```/summer2018/morrison/dataReductionTool``` directory and change the first ```grep``` command for both lines to search for a specific sensor (use sensor names from the downloaded data.csv data set). Change the second ```grep``` command to change which sensor parameter is being searched for. Add (or modify if it already exists) the third ```grep``` command to search for a certain node using the node ID, or remove it to get all nodes with that sensor. Add (or modify if it already exists) a fourth ```grep``` command to search for a specific date and/or time.
8. Continuing to edit graph.sh, change the first line's ```cat``` command file name to be the name of the file just copied (either all of or part of data.csv) and change the second ```cat``` command file name to be the output file name from running the dataReduction.py tool.
9. Run ```./graph.sh``` to generate a plot as a PDF with the file name being the name specified in step 5.

### dataReduction.sh: Data Reduction and Archival Script (Automatic)
1. First follow the instructions listed at this link: https://github.com/waggle-sensor/waggle/tree/master/data to download and unpackage the AoT Chicago Complete node dataset.
2. Then clone this directory: ```git clone https://github.com/waggle-sensor/summer2018.git``` into your home directory.
3. Copy dataReduction.py and dataReduction.sh from the /summer2018/morrison/dataReductionTool directory into the unpackaged AoT Chicago Complete node dataset directory from step 1.
4. Inside the AoT Chicago Complete node dataset directory that you unpackaged in step 1, run the command ```./dataReduction.sh #m``` where ```#``` is an integer and ```m``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively. This command will start the data reduction python script and archive the reduced data set with the metadata files from the downloaded full data set. To only reduce a portion of the data set:
	* Navigate to the unpackaged ```AoT_Chicago.complete.*``` directory.
	* Run ```head -n* data.csv > file_name.csv``` and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the first * lines from the data.csv file into a new file.
	* Or, run ```head -n1 data.csv > file_name.csv```, then ```tail -n* data.csv >> file_name.csv```, and replace ```*``` with the number of lines desired and ```file_name``` with the desired file name to get the last * lines from the data.csv file into a new file.
	* Open dataReduction.sh and replace the input file name (data.csv) for the python3 dataReduction.py command to be the name of the partial data file that you just created.
5. To view and unpackage the files that were just archived, move the newly created ```reducedDataSet.tar.gz``` archive to the desired directory and run the command ```tar -xvf reducedDataSet.tar.gz```.

## Examples

### Data Reduction Over a 10 Min. Period

#### Command:
``` 
waggle-student@ermac:~/summer2018/morrison/dataReductionTool$ python3 dataReduction.py -i smallData.csv -t 10m -o updatedOut.csv
Generating...
Done. Took 43.16s to complete.
```

#### Output:

```
2018/06/13 21:05:00,001e0610e537,alphasense,opc_n2,fw,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,at0,temperature,650.7800000000001,24,27.12
2018/06/13 21:05:00,001e0610e537,chemsense,at1,temperature,659.88,24,27.5
2018/06/13 21:05:00,001e0610e537,chemsense,at2,temperature,676.5800000000002,24,28.19
2018/06/13 21:05:00,001e0610e537,chemsense,at3,temperature,689.3999999999999,24,28.72
2018/06/13 21:05:00,001e0610e537,chemsense,chemsense,id,5410ec38b848,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,co,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,h2s,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,lps25h,pressure,23896.76,24,995.7
2018/06/13 21:05:00,001e0610e537,chemsense,lps25h,temperature,732.7600000000001,24,30.53
2018/06/13 21:05:00,001e0610e537,chemsense,no2,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,o3,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,oxidizing_gases,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,reducing_gases,concentration,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,sht25,humidity,933.75,24,38.91
2018/06/13 21:05:00,001e0610e537,chemsense,sht25,temperature,663.5800000000003,24,27.65
2018/06/13 21:05:00,001e0610e537,chemsense,si1145,ir_intensity,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,si1145,uv_intensity,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,si1145,visible_light_intensity,NA,1,0
2018/06/13 21:05:00,001e0610e537,chemsense,so2,concentration,NA,1,0
...
2018/06/13 21:15:00,001e0610bc12,alphasense,opc_n2,fw,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,at0,temperature,636.1500000000001,24,26.51
2018/06/13 21:15:00,001e0610bc12,chemsense,at1,temperature,644.25,24,26.84
2018/06/13 21:15:00,001e0610bc12,chemsense,at2,temperature,659.14,24,27.46
2018/06/13 21:15:00,001e0610bc12,chemsense,at3,temperature,671.0100000000001,24,27.96
2018/06/13 21:15:00,001e0610bc12,chemsense,chemsense,id,5410ec38a1b,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,co,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,h2s,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,lps25h,pressure,23816.739999999998,24,992.36
2018/06/13 21:15:00,001e0610bc12,chemsense,lps25h,temperature,688.84,24,28.7
2018/06/13 21:15:00,001e0610bc12,chemsense,no2,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,o3,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,oxidizing_gases,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,reducing_gases,concentration,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,sht25,humidity,904.9300000000003,24,37.71
2018/06/13 21:15:00,001e0610bc12,chemsense,sht25,temperature,651.3900000000001,24,27.14
2018/06/13 21:15:00,001e0610bc12,chemsense,si1145,ir_intensity,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,si1145,uv_intensity,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,si1145,visible_light_intensity,NA,1,0
2018/06/13 21:15:00,001e0610bc12,chemsense,so2,concentration,NA,1,0
```

### Data Reduction Over a 1 Hr. Period

#### Command:

```
waggle-student@ermac:~/summer2018/morrison/dataReductionTool$ python3 dataReduction.py -i smallData.csv -t 1h -o updatedOut.csv
Generating...
Done. Took 42.64s to complete.
```

#### Output: 

```
2018/06/13 21:30:00,001e0610e537,alphasense,opc_n2,fw,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,at0,temperature,3887.080000000001,143,27.18
2018/06/13 21:30:00,001e0610e537,chemsense,at1,temperature,3940.7599999999975,143,27.56
2018/06/13 21:30:00,001e0610e537,chemsense,at2,temperature,4039.7199999999993,143,28.25
2018/06/13 21:30:00,001e0610e537,chemsense,at3,temperature,4115.999999999997,143,28.78
2018/06/13 21:30:00,001e0610e537,chemsense,chemsense,id,5410ec38b848,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,co,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,h2s,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,lps25h,pressure,142395.15000000002,143,995.77
2018/06/13 21:30:00,001e0610e537,chemsense,lps25h,temperature,4376.899999999998,143,30.61
2018/06/13 21:30:00,001e0610e537,chemsense,no2,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,o3,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,oxidizing_gases,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,reducing_gases,concentration,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,sht25,humidity,5549.560000000002,143,38.81
2018/06/13 21:30:00,001e0610e537,chemsense,sht25,temperature,3965.2799999999997,143,27.73
2018/06/13 21:30:00,001e0610e537,chemsense,si1145,ir_intensity,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,si1145,uv_intensity,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,si1145,visible_light_intensity,NA,1,0
2018/06/13 21:30:00,001e0610e537,chemsense,so2,concentration,NA,1,0
...
2018/06/13 22:30:00,001e0610e532,chemsense,at0,temperature,4134.76,151,27.38
2018/06/13 22:30:00,001e0610e532,chemsense,at1,temperature,4193.530000000002,151,27.77
2018/06/13 22:30:00,001e0610e532,chemsense,at2,temperature,4303.399999999997,151,28.5
2018/06/13 22:30:00,001e0610e532,chemsense,at3,temperature,4369.729999999999,151,28.94
2018/06/13 22:30:00,001e0610e532,chemsense,chemsense,id,541eec3ebfa6,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,co,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,h2s,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,lps25h,pressure,150534.38,151,996.92
2018/06/13 22:30:00,001e0610e532,chemsense,lps25h,temperature,4592.280000000002,151,30.41
2018/06/13 22:30:00,001e0610e532,chemsense,no2,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,o3,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,oxidizing_gases,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,reducing_gases,concentration,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,sht25,humidity,4951.84,151,32.79
2018/06/13 22:30:00,001e0610e532,chemsense,sht25,temperature,4248.739999999999,151,28.14
2018/06/13 22:30:00,001e0610e532,chemsense,si1145,ir_intensity,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,si1145,uv_intensity,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,si1145,visible_light_intensity,NA,1,0
2018/06/13 22:30:00,001e0610e532,chemsense,so2,concentration,NA,1,0
```

### Data Reduction Over a 1 Day Period (w/ Min-Max in Output)

#### Command:

```
adam@Inspiron:~/summer2018/morrison/dataReductionTool$ python3 dataReduction.py -i node001e0610ba46.csv -t 1d -o updatedOut.csv
Generating...
Done. Took 33.41s to complete.
```

#### Output: 

```
timestamp,node_id,subsystem,sensor,parameter,sum,count,average,min,max
2018/06/09 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_x,-1254095.4310000015,3437,-364.88,-454.545,-272.727
2018/06/09 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_z,-299912.2360000005,3437,-87.26,-294.898,127.551
2018/06/09 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_y,388910.87799999997,3437,113.15,-84.545,299.091
2018/06/09 12:00:00,001e0610ba46,lightsense,tsl260rd,intensity,166445.25400000176,3437,48.43,1.681,84.095
2018/06/09 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_x,-115952.08999999943,3437,-33.74,-56.641,-17.578
2018/06/09 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_y,-3443558.5289999903,3437,-1001.91,-1018.555,-984.375
2018/06/09 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_z,82232.60999999955,3437,23.93,2.93,69.336
2018/06/09 12:00:00,001e0610ba46,metsense,tsl250rd,intensity,43084.6560000003,3437,12.54,0.0,35.5
2018/06/09 12:00:00,001e0610ba46,lightsense,tsl250rd,intensity,150866.39300000112,3437,43.89,1.531,76.218
2018/06/09 12:00:00,001e0610ba46,alphasense,opc_n2,fw,NA,1,0,NA,NA
2018/06/09 12:00:00,001e0610ba46,lightsense,hih6130,humidity,103763.03000000484,3437,30.19,30.19,30.19
2018/06/09 12:00:00,001e0610ba46,lightsense,hih6130,temperature,58429.0,3437,17.0,17.0,17.0
2018/06/09 12:00:00,001e0610ba46,lightsense,ml8511,intensity,155011.48999999958,3437,45.1,42.506,87.5
2018/06/09 12:00:00,001e0610ba46,metsense,hih4030,humidity,259052.33999999662,3437,75.37,61.93,80.05
2018/06/09 12:00:00,001e0610ba46,metsense,tmp112,temperature,67619.97,3437,19.67,15.75,26.94
2018/06/09 12:00:00,001e0610ba46,metsense,htu21d,temperature,66364.36000000002,3437,19.31,15.54,26.42
2018/06/09 12:00:00,001e0610ba46,metsense,htu21d,humidity,236398.95999999915,3437,68.78,49.45,84.53
2018/06/09 12:00:00,001e0610ba46,lightsense,tmp421,temperature,104312.26999999999,3437,30.35,23.25,43.5
2018/06/09 12:00:00,001e0610ba46,metsense,pr103j2,temperature,68041.59999999999,3437,19.8,15.8,27.3
2018/06/09 12:00:00,001e0610ba46,metsense,metsense,id,0111d5141800,1,0,0111d5141800,0111d5141800
...
2018/06/10 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_x,-1261205.4440000015,3438,-366.84,-452.727,-273.636
2018/06/10 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_z,-304473.45000000094,3438,-88.56,-230.612,106.122
2018/06/10 12:00:00,001e0610ba46,lightsense,hmc5883l,magnetic_field_y,390450.0039999999,3438,113.57,-78.182,292.727
2018/06/10 12:00:00,001e0610ba46,lightsense,tsl260rd,intensity,166423.10900000305,3438,48.41,1.676,84.095
2018/06/10 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_x,-113684.56999999912,3438,-33.07,-70.312,34.18
2018/06/10 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_y,-3443936.446000001,3438,-1001.73,-1018.555,-935.547
2018/06/10 12:00:00,001e0610ba46,metsense,mma8452q,acceleration_z,84206.24399999977,3438,24.49,1.953,79.102
2018/06/10 12:00:00,001e0610ba46,metsense,tsl250rd,intensity,28628.41000000006,3438,8.33,0.0,35.449
2018/06/10 12:00:00,001e0610ba46,lightsense,tsl250rd,intensity,150846.26400000084,3438,43.88,1.526,76.218
2018/06/10 12:00:00,001e0610ba46,alphasense,opc_n2,fw,NA,1,0,NA,NA
2018/06/10 12:00:00,001e0610ba46,lightsense,hih6130,humidity,103793.22000000485,3438,30.19,30.19,30.19
2018/06/10 12:00:00,001e0610ba46,lightsense,hih6130,temperature,58446.0,3438,17.0,17.0,17.0
2018/06/10 12:00:00,001e0610ba46,lightsense,ml8511,intensity,151826.66699999964,3438,44.16,42.603,55.292
2018/06/10 12:00:00,001e0610ba46,metsense,hih4030,humidity,257988.53999999733,3438,75.04,62.08,79.91
2018/06/10 12:00:00,001e0610ba46,metsense,tmp112,temperature,69215.28999999992,3438,20.13,16.56,24.12
2018/06/10 12:00:00,001e0610ba46,metsense,htu21d,temperature,67840.51,3438,19.73,16.34,23.59
2018/06/10 12:00:00,001e0610ba46,metsense,htu21d,humidity,266441.0299999998,3438,77.5,63.5,89.59
2018/06/10 12:00:00,001e0610ba46,lightsense,tmp421,temperature,101882.7300000001,3438,29.63,23.81,34.88
2018/06/10 12:00:00,001e0610ba46,metsense,pr103j2,temperature,69510.34999999987,3438,20.22,16.5,24.45
2018/06/10 12:00:00,001e0610ba46,metsense,metsense,id,0111d5141800,1,0,0111d5141800,0111d5141800
2018/06/10 12:00:00,001e0610ba46,metsense,bmp180,temperature,60030.89999999998,3438,17.46,13.9,21.6
```

