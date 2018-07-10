# Custom Plot Generation

## Overview

This tool generates plots based on command line input. Given a directory with data in a file called `data.csv`, as well as metadata files including `nodes.csv`, `sensors.csv`, `provenance.csv` and `README.md`, the tool will extract the requested data from `data.csv` and plot it. The format of the plots can be altered using optional command line arguments.

## Requirements

This tool depends on **python3**, **numpy** and **pandas** packages for python3, as well as **gnuplot**. Please make sure they are installed in the system where they are intended to be used.  
The bash shell scripts this tool uses require a Linux or Mac OS X environment to run.  
The project directory used as input must have the following files:
* `data.csv`
* `nodes.csv`
* `sensors.csv`
* `provenance.csv`
* `README.md`
Plotting also requires that the file `data.csv` has the following columns:
* `timestamp`
* `node_id`
* `subsystem`
* `sensor`
* `paramater`
* One of:
	* `value_hrf`
	* `value_hrf_average`
	* `value_hrf_moving_average`

## How to Use

To retrieve data, go to https://github.com/waggle-sensor/waggle/tree/master/data, download your desired data set, and follow the instructions to decompress the data.  
To get the scripts, clone this repository from `https://github.com/waggle-sensor/data-tools.git`.  
In order to run the scripts, use the command line to navigate to the `plot-data` directory within the repository.  
To generate a simple plot run `python3 gen_custom_plots.py -i data_directory_path -t start_date end_date -p node_id parameter sensor subsystem`  
* `data_directory_path` is the path to the directory created when untaring the archive, or any other directory containing the required files, listed above.  
* `start_date` and `end_date` are dates in the format YYYY-MM-DD. Data is plotted from 00:00:00 on the start date to 23:59:59 on the end date.  
* `node_id` is the id of the node you want to plot data from. A list of nodes can be found in the `nodes.csv` file included with the datasets.
* `parameter`, `sensor` and `subsystem` specify exactly what data you want from the node. A list of these can be found in the `sensors.csv` file included with the datasets.  


For example: `python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02/ -t 2018-06-23 2018-06-23 -p 001e0610ba46 temperature bmp180 metsense`  
This command would generate a plot containing temperature data from the sensor bmp180 in the subsystem metsense for the node 001e0610ba46 from 00:00:00 June 23, 2018 to 23:59:59 June 23, 2018 using the AoT Chicago complete dataset from July 2, 2018.  
The generated plot looks like this:
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/example.png">

## Documentation

### Data Retrieval

https://github.com/waggle-sensor/waggle/tree/master/data contains a list of data sets available for download, as well as instructions on how to decompress the archive.

### Plot Generation

`gen_custom_plots.py` extracts the specified data from `data.csv` in the data directory and combines the data into plottable datasets. Then the data is plotted as specified by command line arguments. The data extracted each time the tool is run is stored in daily slices in a folder called `scratch` in the data directory so that it does not need to be extracted again, because extracting the data can be very time consuming with large datasets. If data is already extracted for a given plot, the files will just be combined into a final plottable dataset. If only some of the specified data is already extracted, the rest of the data will be extracted, skipping over the data that already exists.

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
* `-t` specifies a start date and an end date, defining the time frame over which to plot the data
	* Date format: YYYY-MM-DD
	* Data is plotted from 00:00:00 on the start date to 23:59:59 on the end date
* `-p` specifies the node, parameter, sensor, and subsystem data to plot
	* A list of nodes exists in nodes.csv
	* A list of parameters, sensors and subsystems exists in sensors.csv
* `-n` specifies a node and an ontology to plot
	* Using this option, data from all sensors within the ontology will be plotted on one graph
	* When using a custom layout, 
	* Multiple ontologies van be specified by using the `-n` multiple times
	* In order for a plot to be generated, the node and ontology must be valid:
		* The node must exist in nodes.csv
		* The ontology must exist in sensors.csv

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

#### Examples

##### Simple Plots

###### Example 1
Plot temperature data from sensor bmp180, subsystem metsense, node 001e0610ba46, from 2018-06-20 to 2018-06-23 using data from the AoT Chicago complete dataset.  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -t 2018-06-20 2018-06-23 -p 001e0610ba46 temperature bmp180 metsense`
Will generate terminal output:  
```
Extracting data for all dates in time frame...
Extracting data for 2018/06/17...
Extracting data for node 001e0610ba46 on 2018/06/17...
Extracting temperature data from node 001e0610ba46...
[WARNING] No temperature data from sensor bmp180 in subsystem metsense for node 001e0610ba46 on 2018/06/17 exists
Extracting data for 2018/06/18...
Extracting data for node 001e0610ba46 on 2018/06/18...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/19...
Extracting data for node 001e0610ba46 on 2018/06/19...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/20...
Extracting data for node 001e0610ba46 on 2018/06/20...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/21...
Extracting data for node 001e0610ba46 on 2018/06/21...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/22...
Extracting data for node 001e0610ba46 on 2018/06/22...
Extracting temperature data from node 001e0610ba46...
Extracting data for 2018/06/23...
Extracting data for node 001e0610ba46 on 2018/06/23...
Extracting temperature data from node 001e0610ba46...
Combining data for 001e0610ba46 temperature bmp180 metsense
Plotting data to ./plots/output.png
```  
The warning that no data exists for a certain date lets you know why the plot might not have certain data points.
And generate the following plot:  
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/output.png">

###### Example 2
Plot temperature data from sensor bmp180, subsystem metsense, node 001e0610ba46 and the ontology /sensing/meteorology/temperature for node 001e0610ba8f, from 2018-06-20 to 2018-06-23 to example2.png using data from from the AoT Chicago complete dataset.
The command to generate this plot:  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -o example2.png -t 2018-06-20 2018-06-23 -p 001e0610ba46 temperature bmp180 metsense -n 001e0610ba8f /sensing/meteorology/temperature -e 10`  
The `-e 10` option is needed because otherwise the text for the provenance is too long for the image.  
Will generate terminal output:  
```
Extracting temperature data from node 001e0610ba46...
[WARNING] No temperature data from sensor bmp180 in subsystem metsense for node 001e0610ba46 on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
[WARNING] No temperature data from sensor bmp180 in subsystem metsense for node 001e0610ba8f on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
[WARNING] No temperature data from sensor htu21d in subsystem metsense for node 001e0610ba8f on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
[WARNING] No temperature data from sensor pr103j2 in subsystem metsense for node 001e0610ba8f on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
[WARNING] No temperature data from sensor tmp112 in subsystem metsense for node 001e0610ba8f on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
[WARNING] No temperature data from sensor tsys01 in subsystem metsense for node 001e0610ba8f on 2018/06/17 exists
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Extracting temperature data from node 001e0610ba8f...
Combining data for 001e0610ba46 temperature bmp180 metsense
Combining data for 001e0610ba8f temperature bmp180 metsense
Combining data for 001e0610ba8f temperature htu21d metsense
Combining data for 001e0610ba8f temperature pr103j2 metsense
Combining data for 001e0610ba8f temperature tmp112 metsense
Combining data for 001e0610ba8f temperature tsys01 metsense
Plotting data to ./plots/example2.png
```
The data for node 001e0610ba46 is not extracted because it was stored from when the plot in Example 1 was generated.  


And generate the following plot:  
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/example2.png">

##### Using Plot Settings Arguments

###### Example 3
Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png overlaid in one plot.  
The command to generate this plot:  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -o example3.png -t 2018-06-20 2018-06-23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -v -e 8`  
or  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -o example3.png -t 2018-06-20 2018-06-23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -e 8`  
Either command will work because the tool defaults to overlaying the data.  
Again, the -e option is used so that the command fits in the image.  
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
Extracting data for node 001e0610bbf9 on 2018/06/23...
Extracting pressure data from node 001e0610bbf9...
Extracting humidity data from node 001e0610bbf9...
Extracting data for node 001e0610bc10 on 2018/06/23...
Extracting pressure data from node 001e0610bc10...
Extracting humidity data from node 001e0610bc10...
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
IT WORKS
Plotting data to ./plots/example3.png
```  
And generate the following plot:  
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/example3.png">


###### Example 4
Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png laid out in a 2 by 2 grid.  
The command to generate this plot:  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -o example3.png -t 2018-06-20 2018-06-23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example4.png -l 2 2 -F 12 -e 8`  
The `-F` option is used here to make the titles look nicer and not take up so much room to leave more space for the plots.  
Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example4.png
```
And generate the following plot:  
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/example4.png">

###### Example 5
Plot pressure from sensor bmp180 subsystem metsense for node 001e0610bbf9 and 001e0610bc10 and humidity for sensor htu21d subsystem metsense for node 001e0610bbf9 and 001e0610bc10 from 2018-06-20 to 2018-06-23 to example3.png laid out in a 1 by 4 grid.  
The command to generate this plot:  
`python3 gen_custom_plots.py -i AoT_Chicago.complete.2018-07-02 -o example3.png -t 2018-06-20 2018-06-23 -p 001e0610bbf9 pressure bmp180 metsense -p 001e0610bc10 pressure bmp180 metsense -p 001e0610bbf9 humidity htu21d metsense -p  001e0610bc10 humidity htu21d metsense -o example5-smalltext.png -l 1 4 -F 10 -f 8 -e 7`  
Here, the `-F` and `-f` options are used to keep the plot title from overlapping and to keep the plot keys from going outside their plots.  
Will generate terminal output:  
```
Combining data for 001e0610bbf9 pressure bmp180 metsense
Combining data for 001e0610bbf9 humidity htu21d metsense
Combining data for 001e0610bc10 pressure bmp180 metsense
Combining data for 001e0610bc10 humidity htu21d metsense
Plotting data to ./plots/example5.png
```
And generate the following plot:  
<img src="https://raw.githubusercontent.com/waggle-sensor/data-tools/master/plot-data/examples/example5.png">


When plotting ontologies using `-n`, each ontology will be plotted in 1 plot. So if you wanted to plot 3 things with `-p` and 1 ontology in a 2 by 2 layout, there would be 3 plots containing one dataset and one containing all the data for the ontology.  

If you want to trim outlying data (greater than 3 or -3 standard deviations away from the mean) you can use the `-r` option.  
If you want to plot data using a log scale, you can use the `-s` option.



