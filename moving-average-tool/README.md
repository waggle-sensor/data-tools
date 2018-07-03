# Moving Averages Command Line Tool

## Requirements
This tool requires that the user has Python3 installed, and was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic. It has also been tested on an Apple Macbook and worked correctly.

## Description
This tool will calculate a simple moving average from a complete node data set by averaging sensor values for time ranged windows specified by the user.

The command line tool movingAvg.py takes in a directory path and a time period. The directory path must be the full path to an unpackaged complete node data set (data sets located here: https://github.com/waggle-sensor/waggle/tree/master/data). This path must must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv. The tool will confirm that the aformentioned files exist in the passed in directory before allowing the user to begin reducing data. The time period specified determines the time range window for calculating a simple moving average (e.g. over a span of 5 mins., 1 hr., 1 day, etc.). This time ranged window will move through the data in the data.csv file. For each sensor on each node, the tool will append new sensor values to the time ranged window and throw away values outside of the time ranged window. It will constantly calculate the average of the values in this window, which becomes the simple moving average as it parses through the data. 

This tool will read the data.csv file located in the passed in directory path, parse through the large data.csv data set, and create moving averages for pieces of data (sensor values) over the time range window period given by the user. It will then create a new movingAvgData.csv file. The final output of the movingAvg.py tool will be a sub directory placed in the passed in directory that contains the moving average data set (moving avgerage data.csv) and the extra metadata files (nodes.csv, provenance.csv, and sensors.csv), along with a modified README (README.md,) from the passed in unpackaged complete node data set directory path.

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

## Example

### Moving Average Over a 5 Min. Period
```
waggle-student@ermac:~/data-tools/moving-average-tool$ python3 movingAvg.py -i /home/waggle-student/Downloads/AoT_Portland.complete.2018-07-03/ -t 5m
Generating...
Done. Took 1579.22s to complete.
waggle-student@ermac:~/Downloads/AoT_Portland.complete.2018-07-03/AoT_Portland.complete.2018-07-03_moving_average_data_5m$ tail -n100 data.csv 
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,fw,218.39999999999995,12,18.199999999999996
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,id,OPC-N2 176180608    ,0,OPC-N2 176180608
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,pm1,0.273,12,0.022750000000000003
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,pm10,0.34700000000000003,12,0.02891666666666667
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,pm2_5,0.34400000000000003,12,0.02866666666666667
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,sample_flow_rate,35.448769999999996,12,2.9540641666666665
2018/07/02 23:58:38,001e06113a07,alphasense,opc_n2,sampling_period,302.7864900000001,12,25.232207500000005
2018/07/02 23:58:38,001e06113a07,chemsense,at0,temperature,323.39,12,26.949166666666667
2018/07/02 23:58:38,001e06113a07,chemsense,at1,temperature,330.86,12,27.57166666666667
2018/07/02 23:58:38,001e06113a07,chemsense,at2,temperature,344.64,12,28.72
2018/07/02 23:58:38,001e06113a07,chemsense,at3,temperature,356.41999999999996,12,29.701666666666664
2018/07/02 23:58:38,001e06113a07,chemsense,chemsense,id,5410ec38a76e,0,5410ec38a76e
2018/07/02 23:58:38,001e06113a07,chemsense,co,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,h2s,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,lps25h,pressure,12257.24,12,1021.4366666666666
2018/07/02 23:58:38,001e06113a07,chemsense,lps25h,temperature,367.04999999999995,12,30.587499999999995
2018/07/02 23:58:38,001e06113a07,chemsense,no2,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,o3,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,oxidizing_gases,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,reducing_gases,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,sht25,humidity,322.56,12,26.88
2018/07/02 23:58:38,001e06113a07,chemsense,sht25,temperature,336.0,12,28.0
2018/07/02 23:58:38,001e06113a07,chemsense,si1145,ir_intensity,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,si1145,uv_intensity,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,si1145,visible_light_intensity,NA,0,NA
2018/07/02 23:58:38,001e06113a07,chemsense,so2,concentration,NA,0,NA
2018/07/02 23:58:38,001e06113a07,lightsense,apds_9006_020,intensity,9.486000000000002,12,0.7905000000000002
2018/07/02 23:58:38,001e06113a07,lightsense,hih6130,humidity,138.75,12,11.5625
2018/07/02 23:58:38,001e06113a07,lightsense,hih6130,temperature,608.4699999999999,12,50.705833333333324
2018/07/02 23:58:38,001e06113a07,lightsense,hmc5883l,magnetic_field_x,-2658.182,12,-221.51516666666666
2018/07/02 23:58:38,001e06113a07,lightsense,hmc5883l,magnetic_field_y,1108.1799999999998,12,92.34833333333331
2018/07/02 23:58:38,001e06113a07,lightsense,hmc5883l,magnetic_field_z,3776.531,12,314.71091666666666
2018/07/02 23:58:38,001e06113a07,lightsense,ml8511,intensity,482.25199999999995,12,40.187666666666665
2018/07/02 23:58:38,001e06113a07,lightsense,mlx75305,intensity,155.676,12,12.972999999999999
2018/07/02 23:58:38,001e06113a07,lightsense,tmp421,temperature,572.28,12,47.69
2018/07/02 23:58:38,001e06113a07,lightsense,tsl250rd,intensity,3.3139999999999996,12,0.2761666666666666
2018/07/02 23:58:38,001e06113a07,lightsense,tsl260rd,intensity,36.602000000000004,12,3.050166666666667
2018/07/02 23:58:38,001e06113a07,metsense,bmp180,pressure,11558.730000000001,12,963.2275000000001
2018/07/02 23:58:38,001e06113a07,metsense,bmp180,temperature,641.1,12,53.425000000000004
2018/07/02 23:58:38,001e06113a07,metsense,hih4030,humidity,563.85,12,46.987500000000004
2018/07/02 23:58:38,001e06113a07,metsense,htu21d,humidity,233.43,12,19.4525
2018/07/02 23:58:38,001e06113a07,metsense,htu21d,temperature,315.96999999999997,12,26.33083333333333
2018/07/02 23:58:38,001e06113a07,metsense,metsense,id,01d0e0e21700,0,01d0e0e21700
2018/07/02 23:58:38,001e06113a07,metsense,mma8452q,acceleration_x,23.438,12,1.9531666666666665
2018/07/02 23:58:38,001e06113a07,metsense,mma8452q,acceleration_y,257.812,12,21.484333333333336
2018/07/02 23:58:38,001e06113a07,metsense,mma8452q,acceleration_z,-11809.570000000002,12,-984.1308333333335
2018/07/02 23:58:38,001e06113a07,metsense,pr103j2,temperature,331.65000000000003,12,27.637500000000003
2018/07/02 23:58:38,001e06113a07,metsense,spv1840lr5h_b,intensity,817.8800000000001,12,68.15666666666668
2018/07/02 23:58:38,001e06113a07,metsense,tmp112,temperature,323.01,12,26.9175
2018/07/02 23:58:38,001e06113a07,metsense,tsl250rd,intensity,59.971999999999994,12,4.9976666666666665
2018/07/02 23:58:38,001e06113a07,metsense,tsys01,temperature,327.25,12,27.270833333333332

```
