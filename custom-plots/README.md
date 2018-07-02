# Custom Plot Generation

This tool generates custom plots based on command line input. It retrieves the complete data set, then extracts the data for the desired parameters and time frame, then plots the data.

This tool relies on `plotting utilities.py`, `extract.sh` and `cut.sh` in the parent directory. It also requires the pandas and numpy packages for python.

To retrieve data run `./data/fileMaker.sh`
To generate plots run `python3 gen_custom_plots.py ...` 

## Data Retrieval

`fileMaker.sh` downloads and uncompresses the complete data set, then cuts the data into slices of the last 30 days, last 7 days and last 1 day. `gen_custom_plots.py` will further reduce the data.

## Plot Generation

`gen_custom_plots.py` extracts the specified data from the files created by `fileMaker.sh` and combines the data into plottable datasets. Then the data is plotted as specified by command line arguments. The data extracted each time the tool is run is stored in daily slices so that it does not need to be extracted again, because extracting the data is very time consuming. If data is already extracted for a given plot, the files will just be combined into a final plottable dataset. If only some of the specified data is already extracted, the rest of the data will be extracted, skipping over the data that already exists.

### Command Line Arguments

#### Plot Data Arguments

The arguments needed to generate a plot are `-p` (`--plot`), `-t` (`--timeframe`) and `-o` (`--output`)
* `-p` specifies the node, parameter, sensor, and subsystem data to plot
	* At least one node, parameter, sensor, subsystem quadruplet must be specified to generate a plot
	* Multiple quadruplets can be specified by using the `-p` argument multiple times
	* In order for a plot to be generated, the quadruplet must be valid
		* A quadruplet is valid if:
			* The node exists in nodes.csv
			* The parameter exists in sensors.csv
			* The sensor measures the parameter
			* The sensor belongs to the subsystem
* `-t` specifies a start date and an end date, defining the time frame over which to plot the data
	* Date format: YYYY/MM/DD
	* Data is plotted from 00:00:00 on the start date to 23:59:59 on the end date
	* A valid time frame is required to generate a plot
		* A time frame is valid if:
			* Both the start date and the end date have the correct date format
			* The start date is earlier than or the same as the end date
			* Both the start and date exist in the data sets
* `-o` specifies the output file name
	* If this argument is not provided, a default file name will be used
	* The default file name is 'output.png'

#### Plot Settings Arguments

These arguments determine how the data will be displayed in the plot: `-v` (`--overlay`), `-l` (`--layout`), `-r` (`--trim`), `-s` (`--logscale`), `-F` (`--titlefont`), `-f` (`--plotfont`)
* `-v` overlays all of the data in one plot
	* This is the default behavior if no layout is specified
	* If multiple parameters are being plotted, there can be a maximum of two different units associated with those parameters for this option to work (e.g. temperature has unit 'C', humidity has unit 'RH' and pressure has unit 'hPa', temperature and humidity could be plotted in one plot, but temperature, humidity and pressure could not be)
	* Cannot be used in conjunction with `l`
* `-l` specifies a the number of rows and columns of plots
	* The default layout is 1 by 1
	* The product of rows and columns cannot be less than the number of plots
	* Cannot be used in conjunction with `-v`
* `-r` trims outlying data points (>±3σ)
* `-s` plots data using a log scale for the y axis
* `-F` sets the font size for plot titles and provenance, the default size is 12
* `-f` sets the font size for plot keys and axis labels, the default size is 10

#### Optional Arguments

To get help for this tool use `-h` (`--help`)
* `-h` shows a help message and exits

### Usage

#### Help (`-h`)
`python3 gen_custom_plots.py -h` produces the following output:
```
usage: gen_custom_plots.py [-h] [-t start_date end_date]
                           [-p node_id parameter sensor subsystem] [-o OUTPUT]
                           [-v] [-l rows columns] [-r] [-s] [-F TITLEFONT]
                           [-f PLOTFONT]

Generate custom data sets and plots

plot data arguments:
  -t start_date end_date, --timeframe start_date end_date
                        timeframe for which to plot data, date format =
                        YYYY/MM/DD
  -p node_id parameter sensor subsystem, --plot node_id parameter sensor subsystem
                        node id, parameter, sensor, and subsystem to plot
  -o OUTPUT, --output OUTPUT
                        output file name, default name is output.png, files
                        are written to ./plots/

plot settings arguments:
  -v, --overlay         overlay data in one plot, cannot be used with -l
                        (--layout) option
  -l rows columns, --layout rows columns
                        specify the number of rows and columns of plots,
                        cannot be used with -v (--overlay) option
  -r, --trim            trim outlying data points (>±3σ)
  -s, --logscale        plot data using a log scale for the y axis
  -F TITLEFONT, --titlefont TITLEFONT
                        font size for plot titles
  -f PLOTFONT, --plotfont PLOTFONT
                        font size for text inside the plot

optional arguments:
  -h, --help            show this help message and exit

```

#### Simple Plots

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

#### Using Plot Settings Arguments

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



