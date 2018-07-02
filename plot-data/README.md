# Custom Plot Generation

## Overview

This tool generates plots based on command line input. Given a directory with data in a file called `data.csv`, as well as metadata files including `nodes.csv`, `sensors.csv`, `provenance.csv` and `README.md`, the tool will extract the requested data from `data.csv` and plot it. The format of the plots can be altered using optional command line arguments.

## Requirements

This tool depends on **python3**, **numpy** and **pandas** packages for python3, as well as **gnuplot**. Please make sure they are installed in the system where they are intended to be used.  
The bash shell scripts this tool uses require a Linux or Mac OS X environment to run.

## How to Use

To retrieve data, go to https://github.com/waggle-sensor/waggle/tree/master/data, download your desired data set, and follow the instructions to decompress the data.  
To generate a simple plot run `python3 gen_custom_plots.py -i data_directory_path -t start_date end_date -p node_id parameter sensor subsystem`  
`data_directory_path` is the path to the directory created when untaring the archive, or any other directory containing the required files, listed above.  
`start_date` and `end_date` are dates in the format YYYY-MM-DD. Data is plotted from 00:00:00 on the start date to 23:59:59 on the end date.  
`node_id` is the id of the node you want to plot data from. A list of nodes can be found in the `nodes.csv` file included with the datasets.
`parameter`, `sensor` and `subsystem` specify exactly what data you want from the node. A list of these can be found in the `sensors.csv` file included with the datasets.

## Documentation

### Data Retrieval

https://github.com/waggle-sensor/waggle/tree/master/data contains a list of data sets available for download, as well as instructions on how to decompress the archive.

### Plot Generation

`gen_custom_plots.py` extracts the specified data from the files created by `fileMaker.sh` and combines the data into plottable datasets. Then the data is plotted as specified by command line arguments. The data extracted each time the tool is run is stored in daily slices so that it does not need to be extracted again, because extracting the data is very time consuming. If data is already extracted for a given plot, the files will just be combined into a final plottable dataset. If only some of the specified data is already extracted, the rest of the data will be extracted, skipping over the data that already exists.

#### Command Line Arguments

##### Plot Data Arguments

The arguments needed to generate a plot are `-i` (`--input`), `-o` (`--output`), `-t` (`--timeframe`) and `-p` (`--plot`)
* `-i` specifies the directory that contains `data.csv` and the necessary metadata
	* Required files in input directory:
		* `data.csv`
		* `nodes.csv`
		* `sensors.csv`
		* `provenance.csv`
		* `README.md`
* `-o` specifies the output file name
	* If this argument is not provided, a default file name will be used
	* The default file name is 'output.png'
* `-p` specifies the node, parameter, sensor, and subsystem data to plot
	* A list of nodes exists in nodes.csv
	* A list of parameters, sensors and subsystems exists in sensors.csv
* `-t` specifies a start date and an end date, defining the time frame over which to plot the data
	* Date format: YYYY-MM-DD
	* Data is plotted from 00:00:00 on the start date to 23:59:59 on the end date

##### Plot Settings Arguments

These arguments determine how the data will be displayed in the plot: `-v` (`--overlay`), `-l` (`--layout`), `-m` (`--trim`), `-s` (`--logscale`), `-F` (`--titlefont`), `-f` (`--plotfont`), `-r` (`--resolution`), `-a` (`--address`)
* `-v` overlays all of the data in one plot
	* This is the default behavior if no layout is specified
	* If multiple parameters are being plotted, there can be a maximum of two different units associated with those parameters for this option to work (e.g. temperature has unit 'C', humidity has unit 'RH' and pressure has unit 'hPa', temperature and humidity could be plotted in one plot, but temperature, humidity and pressure could not be)
	* Cannot be used in conjunction with `l`
* `-l` specifies the number of rows and columns of plots
	* The default layout is 1 by 1
	* The product of rows and columns must be greater than or equal to the number of plots
	* Cannot be used in conjunction with `-v`
* `-m` trims outlying data points (>±3σ)
* `-s` plots data using a log scale for the y axis
* `-F` sets the font size for plot titles and provenance, the default size is 12
* `-f` sets the font size for plot keys and axis labels, the default size is 10
* `-r` sets the resolution for the output image
* `-a` sets the source address of the data for the plot provenance

##### Optional Arguments

To get help for this tool use `-h` (`--help`)
* `-h` shows a help message and exits

#### Usage

##### Help (`-h`)
`python3 gen_custom_plots.py -h` produces the following output:
```
usage: gen_custom_plots.py [-h] -i INPUT [-o OUTPUT] -t start_date end_date
                           [-p node_id parameter sensor subsystem]
                           [-n node_id ontology] [-v] [-l rows columns] [-m]
                           [-s] [-F TITLEFONT] [-f PLOTFONT]
                           [-e PROVENANCEFONT] [-r width,height width,height]
                           [-a ADDRESS]

Generate custom data sets and plots

plot data arguments:
  -i INPUT, --input INPUT
                        input directory path
  -o OUTPUT, --output OUTPUT
                        output file name, default name is output.png, files
                        are written to input_path/plots/
  -t start_date end_date, --timeframe start_date end_date
                        timeframe for which to plot data, date format = YYYY-
                        MM-DD
  -p node_id parameter sensor subsystem, --plot node_id parameter sensor subsystem
                        node id, parameter, sensor, and subsystem to plot,
                        either this option or -n (--ontology) is required to
                        generate a plot
  -n node_id ontology, --ontology node_id ontology
                        specify a node and an ontology to plot all of the data
                        for on one graph, either this option or -p (--plot) is
                        required to generate a plot

plot settings arguments:
  -v, --overlay         overlay data in one plot, cannot be used with -l
                        (--layout) option
  -l rows columns, --layout rows columns
                        specify the number of rows and columns of plots,
                        cannot be used with -v (--overlay) option
  -m, --trim            trim outlying data points (>±3σ)
  -s, --logscale        plot data using a log scale for the y axis
  -F TITLEFONT, --titlefont TITLEFONT
                        font size for plot titles, default = 16
  -f PLOTFONT, --plotfont PLOTFONT
                        font size for text inside the plot, default = 12
  -e PROVENANCEFONT, --provenancefont PROVENANCEFONT
                        font size for plot provenance, default = 14
  -r width,height width,height, --resolution width,height width,height
                        resolution of output png (width,height)
  -a ADDRESS, --address ADDRESS
                        source address of the data to be included in the plot
                        provenance

optional arguments:
  -h, --help            show this help message and exit
```

##### Simple Plots

Example 1: Plot temperature data from sensor bmp180, subsystem metsense, node 001e0610ba46, from 2018-06-20 to 2018-06-23. 
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610ba46 temperature bmp180 metsense`  
Will generate terminal output:  
```
Extracting data for all dates in time frame...
Extracting data for node 001e0610ba46 on 2018/06/20...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/21...
Extracting data for node 001e0610ba46 on 2018/06/21...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/22...
Extracting data for node 001e0610ba46 on 2018/06/22...
Extracting temperature data from node 001e0610ba46...
Extracting data for node 001e0610ba46 on 2018/06/23...
Extracting temperature data from node 001e0610ba46...
Combining data for 001e0610ba46 temperature bmp180 metsense
Plotting data to ./plots/output.png
```  
And generate the following plot:  
![output.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/output.png)  
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/output.png?token=AUW0UvvYalBBgwjTQBNj6FSa1vF0Fpnmks5bPT9BwA%3D%3D">

Example 2: Plot temperature data from sensor bmp180, subsystem metsense, node 001e0610ba46 and node 001e0610ba8f, from 2018-06-20 to 2018-06-23 to example2.png.
The command to generate this plot:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610ba46 temperature bmp180 metsense -p 001e0610ba8f temperature bmp180 metsense -o example2.png`  
Will generate terminal output:  
```
Extracting data for node 001e0610ba8f on 2018/06/20...
Extracting temperature data from node 001e0610ba8f...
Extracting data for node 001e0610ba8f on 2018/06/21...
Extracting temperature data from node 001e0610ba8f...
Extracting data for node 001e0610ba8f on 2018/06/22...
Extracting temperature data from node 001e0610ba8f...
Extracting data for node 001e0610ba8f on 2018/06/23...
Extracting temperature data from node 001e0610ba8f...
Combining data for 001e0610ba46 temperature bmp180 metsense
Combining data for 001e0610ba8f temperature bmp180 metsense
Plotting data to ./plots/example2.png
```
The data for node 001e0610ba46 is not extracted because it was stored from when the plot in Example 1 was generated.  
And generate the following plot:  
![example2.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example2.png)  
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example2.png?token=AUW0Ur0XhNAzABN0xcQKDru_vkjuiw14ks5bPUBNwA%3D%3D">

##### Using Plot Settings Arguments

Example 3: Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png overlaid in one plot.  
The command to generate this plot:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example3.png -v`  
or  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example3.png`  
Either command will work because the tool defaults to overlaying the data.  
Will generate terminal output:  
```
Extracting data for node 001e0610bbf9 on 2018/06/20...
Extracting pressure data from node 001e0610bbf9...
Extracting humidity data from node 001e0610bbf9...
Extracting data for node 001e0610bc10 on 2018/06/20...
Extracting pressure data from node 001e0610bc10...
Extracting humidity data from node 001e0610bc10...
Extracting data for node 001e0610bbf9 on 2018/06/21...
Extracting pressure data from node 001e0610bbf9...
Extracting humidity data from node 001e0610bbf9...
Extracting data for node 001e0610bc10 on 2018/06/21...
Extracting pressure data from node 001e0610bc10...
Extracting humidity data from node 001e0610bc10...
Extracting data for node 001e0610bbf9 on 2018/06/22...
Extracting pressure data from node 001e0610bbf9...
Extracting humidity data from node 001e0610bbf9...
Extracting data for node 001e0610bc10 on 2018/06/22...
Extracting pressure data from node 001e0610bc10...
Extracting humidity data from node 001e0610bc10...
Extracting pressure data from node 001e0610bbf9...
Extracting humidity data from node 001e0610bbf9...
Extracting pressure data from node 001e0610bc10...
Extracting humidity data from node 001e0610bc10...
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/output.png
```
And generate the following plot:  
![example3.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example3.png)  
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example3.png?token=AUW0UvJfT41l8Vs6f3DyZDuKjgq6aS8Oks5bPUYUwA%3D%3D">

The command for this plot does not quite fit on the plot, so we can change the size of the plot title to make it fit using the `-F` option:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example3-smalltitle.png -v -F 12`  
Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example3-smalltitle.png
```
And generate the following plot:  
![example3-smalltitle.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example3-smalltitle.png)
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example3-smalltitle.png?token=AUW0Urm9ZYgR16hVwrUOOQpAwx1RCW6nks5bPUZgwA%3D%3D">

Example 4: Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png laid out in a 2 by 2 grid.  
The command to generate this plot:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example4.png -l 2 2 -F 12`  
The `-F` option is used here again because the command is similar in length to example 3, so we want it to fit the first time.
Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example4.png
```
And generate the following plot:  
![example4.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example4.png)  
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example4.png?token=AUW0UkmJmuJjMsSWv0xVmxiUMShsVQvcks5bPUgxwA%3D%3D">

Example 5: Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png laid out in a 1 by 4 grid.  
The command to generate this plot:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example5.png -l 1 4 -F 12`  

Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example5.png
```
And generate the following plot:  
![example5.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example5.png) 
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example5.png?token=AUW0Un4aWKgWrrqJvNifnvyjCEbYXvF9ks5bPUsQwA%3D%3D"> 

Both the titles of the plots and the text within the plots are too large, so we need to decrease the font size of both using `-F` for the titles, and `-f` for the plot text:  
`python3 gen_custom_plots.py -t 2018/06/20 2018/06/23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example5-smalltext.png -l 1 4 -F 10 -f 8`  
Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example5-smalltext.png
```
And generate the following plot:  
![example5-smalltext.png](https://github.com/waggle-sensor/summer2018/tree/master/dawnkaski/custom_plots/examples/example5-smalltext.png)  
<img src="https://raw.githubusercontent.com/waggle-sensor/summer2018/master/dawnkaski/custom_plots/examples/example5-smalltext.png?token=AUW0UhNoqOKXigc0IxxHkVy76bcOtms2ks5bPUtWwA%3D%3D">  


If you want to trim outlying data (greater than 3 standard deviations away from the mean) you can use the `-r` option.  
If you want to plot data using a log scale, you can use the `-s` option.



