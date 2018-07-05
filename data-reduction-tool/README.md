# Data Reduction Command Line Tool

## Requirements
This tool requires Python3.

## Step-by-Step Instructions for Reducing Data
1. Download and unpackage a complete node dataset. Make sure to complete the step that unpackages the data.csv.gz archive.
2. Run the dataReduction.py tool from the command line:

```python3 dataReduction.py -i /PATH_TO_COMPLETE_NODE_DATA_SET -t #x```

Replace ```/PATH_TO_COMPLETE_NODE_DATA_SET``` with the path to the unpackaged compete node data set from step 1, ```#``` with an integer and ```x``` with one of the following characters: ```'s','m','h', or 'd'```. The ```-v #``` option with ```#``` replaced by an integer can be used to print a line count after every ```#``` number of lines have been parsed (this causes the progam to take more time to reduce data). 

## Examples

### Data Reduction Over a 10 Min. Period

#### Command:
``` 
ermac:~/data-tools/data-reduction-tool$ python3 dataReduction.py -i ../AoT_Chicago.complete.2018-06-19 -t 10m
Generating...
Done. Took 7.01s to complete.
```

#### Reduced Data Output:

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
ermac:~/data-tools/data-reduction-tool$ python3 dataReduction.py -i ../AoT_Chicago.complete.2018-06-19 -t 1h
Generating...
Done. Took 6.77s to complete.
```

#### Reduced Data Output: 

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
ermac:~/data-tools/data-reduction-tool$ python3 dataReduction.py -i ../AoT_Chicago.complete.2018-06-19 -t 1d
Generating...
Done. Took 7.03s to complete.
```

#### Reduced Data Output: 

```
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

## Detailed Description
This tool will reduce the amount of data from a complete node data set by averaging sensor values over a specified time period.

### Input: 
The command line tool `dataReduction.py` takes in a directory path and a time period. The directory path must be the full path to an unpackaged complete node data set (data sets located here: https://github.com/waggle-sensor/waggle/tree/master/data). This path must must contain the files: data.csv(uncompress the data.csv.gz file before using the tool), nodes.csv, provenance.csv, README.md, and sensors.csv. The tool will confirm that the aformentioned files exist in the passed in directory before allowing the user to begin reducing data. The time period specified by the user determines the "bucket" range of values for averaging (i.e. if the user specifies 1 day, all of the values for each sensor on each node will be reduced to a single timestamp for each day).

### Output:
This tool will read the data.csv file located in the provided directory path, and reduce the amount of data by averaging/combining pieces of data (sensor values) over the time period given by the user. It will then create a sub directory inside the source directory with reduced data set (reduced) data.csv and extra metadata files 
(nodes.csv, provenance.csv, and sensors.csv) along with a modified README (README.md). In the reduction process, the timestamps are written out as halfway between the interval specified by the user

## How to Use dataReduction.py

When typing on the terminal, the tool takes in two required parameters (input directory path and time period) with identifiers and one optional parameter (verbose) with an identifier: input directory path (```-i, --input```), time period (```-t, --time```) and verbose option for number of lines parsed (```-v, --verbose```).

**Input:** The path to the unpackaged complete node data set (must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv).

**Period:** The period parameter should be in the format ```-t #x ``` where ```#``` is an integer and ```x``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively.

**Verbose:** Optional parameter. Specifying the verbose option with an integer will print out the number of lines parsed for every increment of the integer passed in (e.g. if user enters 1000, every 1000 lines the program will print the number of lines - 1000, 2000, 3000...)

**Note:** User is not allowed to enter anything less than 24 seconds because it is how often data is received and an average could not be calculated for anything lower.
**Note:** The reduced data.csv output file will have the headers: ```timestamp,node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_average``` all the time. If there are more than a certain number of values (1000 right now) in any of the averaging periods, the tool will output the reduced data.csv file with the headers: ```timestamp,node_id,subsystem,sensor,parameter,value_hrf__sum,value_hrf_count,value_hrf_average,value_hrf__min,value_hrf_max```. It includes a minimum and maximum value per averaging period that is useful when graphing or analyzing the output data.

Terminal command format should be like these examples: ```python3 dataReduction.py -i /home/waggle-student/Downloads/AoT_Chicago.complete.2018-06-19 -t 30m``` or ```python3 dataReduction.py -i /home/waggle-student/Downloads/AoT_Chicago.complete.2018-06-19 -t 30m -v 1000```

Typing ```-h``` or ```--help``` as a parameter when using this tool will pull up the help: ```python3 dataReduction.py -h```.

Errors will be specified for user error such as: not all of the parameters being filled in when using the tool, not specifying an input file, specifying an input or output file that is not .csv format, etc.


### Compatibility
This tool was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic. It has also been tested on an Apple Macbook and worked correctly.

