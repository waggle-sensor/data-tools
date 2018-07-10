#!/usr/bin/env python3

import subprocess
import argparse
import datetime
import shutil
import pandas
import numpy
import sys
import re
import os

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
utils = os.path.join(parent,'utils')
sys.path.append(utils)

from plotting_utilities import *
from collections import OrderedDict

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("[ERROR] {} is invalid, format should be YYYY-MM-DD".format(date_text))
        exit(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate custom data sets and plots')
	optional = parser._action_groups.pop()
	data = parser.add_argument_group('plot data arguments')
	settings = parser.add_argument_group('plot settings arguments')
	data.add_argument('-i', '--input', help='input directory path', required=True)
	data.add_argument('-o', '--output', default='output.png', help='output file name, default name is output.png, files are written to input_path/plots/')
	data.add_argument('-t', '--timeframe', metavar=('start_date', 'end_date'), nargs=2, help='timeframe for which to plot data, date format = YYYY-MM-DD', required=True)
	data.add_argument('-p', '--plot', metavar=('node_id','parameter','sensor','subsystem'), action='append', nargs=4, help='node id, parameter, sensor, and subsystem to plot, either this option or -n (--ontology) is required to generate a plot')
	data.add_argument('-n', '--ontology', metavar=('node_id','ontology'), action ='append', nargs=2, help='specify a node and an ontology to plot all of the data for on one graph, either this option or -p (--plot) is required to generate a plot')
	settings.add_argument('-v', '--overlay', action='store_true', help='overlay data in one plot, cannot be used with -l (--layout) option')
	settings.add_argument('-l', '--layout', default=[1,1], metavar=('rows', 'columns'), nargs=2, type=int, help='specify the number of rows and columns of plots, cannot be used with -v (--overlay) option')
	settings.add_argument('-m', '--trim', action='store_true', help='trim outlying data points (>±3σ)')
	settings.add_argument('-s', '--logscale', action='store_true', help='plot data using a log scale for the y axis')
	settings.add_argument('-F', '--titlefont', default=[16], nargs=1, type=int, action='store', help='font size for plot titles, default = 16')
	settings.add_argument('-f', '--plotfont', default=[12], nargs=1, type=int, action='store', help='font size for text inside the plot, default = 12')
	settings.add_argument('-e', '--provenancefont', default=[14], nargs = 1, type=int, action='store', help='font size for plot provenance, default = 14')
	settings.add_argument('-r', '--resolution', default=[1920,1080], metavar=('width,height'), nargs=2, type=int, help='resolution of output png (width,height)')
	settings.add_argument('-a', '--address', help='source address of the data to be included in the plot provenance')
	parser._action_groups.append(optional)

	args = parser.parse_args()

	cwd = os.getcwd()

	if args.input is None:
		print('[ERROR] no input directory specified')
		parser.print_help()
		exit(1)

	data_directory = os.path.abspath(args.input)
	if not os.path.exists(data_directory):
		print('[ERROR] input path does not exist')
		exit(1)

	required_files = ['data.csv','nodes.csv','sensors.csv','provenance.csv','README.md']
	exit_flag = False
	for file in required_files:
		file_path = os.path.join(data_directory,file)
		if not os.path.exists(file_path):
			print('[ERROR] {} does not exist in the input path'.format(file))
			exit_flag = True
	if exit_flag:
		exit(1)


	dicts = getNodes(data_directory)
	nodes_dict = dicts[0]
	details_dict = dicts[1]

	dicts = getSensors(data_directory)
	parameter_to_sensor_subsystem_dict = dicts[0]

	ontology_dict = dicts[1]
	triplet_to_hrf_unit_dict = dicts[4]

	p = re.compile('\.png$')
	m = p.search(args.output)
	if not m:
		print('[ERROR] output file {} is not a png'.format(args.output))
		exit(1)

	if '/' in args.output or '\\' in args.output:
		print('[ERROR] illegal character in output file name')
		exit(1)

	datacsv_path = os.path.join(data_directory,'data.csv')
	earliest_date = getStartDate(datacsv_path)
	latest_date = getEndDate(datacsv_path)

	exit_flag = False
	if args.plot is None and args.ontology is None:
		print('[ERROR] No plot data specified')
		exit_flag = True
	if args.timeframe is None:
		print('[ERROR] No time frame specified')
		exit_flag = True
	if exit_flag:
		parser.print_help()
		exit(1)

	if args.overlay and args.layout != [1,1]:
		print('[ERROR] Cannot use both -v (--overlay) and -l (--layout) options')
		exit(1)

	a = 0
	b = 0
	if args.plot:
		a = len(args.plot)
	if args.ontology:
		b = len(args.ontology)
	total = a+b
	if args.layout != [1,1] and total > args.layout[0]*args.layout[1]:
		print('[ERROR] {} plots will not fit in a {} by {} layout'.format(total,args.layout[0],args.layout[1]))
		exit(1)

	validate(args.timeframe[0])
	validate(args.timeframe[1])
	p = re.compile('\d{4}-\d{2}-\d{2}')
	m0 = p.match(args.timeframe[0])
	m1 = p.match(args.timeframe[1])
	if not m0:
		print('[ERROR] Start date: "{}" does not match date format YYYY/MM/DD'.format(args.timeframe[0]))
	if not m1:
		print('[ERROR] Start date: "{}" does not match date format YYYY/MM/DD'.format(args.timeframe[1]))
	if not m0 or not m1:
		exit(1)

	if args.timeframe[0] > args.timeframe[1]:
		print('[ERROR] Start date is greater than end date')
		exit(1)

	start_date = '{} 00:00:00'.format(args.timeframe[0].replace('-','/'))
	end_date = '{} 23:59:59'.format(args.timeframe[1].replace('-','/'))

	if (start_date < earliest_date):
		print('[ERROR] Start date is earlier than the earliest date in data.csv')
	if (end_date > latest_date):
		print('[ERROR] End date is later than the latest date in data.csv')
	if ((start_date < earliest_date) or (end_date > latest_date)):
		exit(1)

	exit_flag = False
	if args.plot:
		for quadruplet in args.plot:
			if quadruplet[0] not in nodes_dict:
				print('[ERROR] Node: {} does not exist in nodes.csv'.format(quadruplet[0]))
				exit_flag = True
			if quadruplet[1] not in parameter_to_sensor_subsystem_dict:
				print('[ERROR] Parameter: {} does not exist in sensors.csv'.format(quadruplet[1]))
				exit_flag = True
			valid_sensor_flag = False
			valid_subsystem_flag = False
			if quadruplet[1] in parameter_to_sensor_subsystem_dict:
				for triplet in parameter_to_sensor_subsystem_dict[quadruplet[1]]:
					if quadruplet[2] in triplet:
						valid_sensor_flag = True
					if quadruplet[3] in triplet:
						valid_subsystem_flag = True
				if not valid_sensor_flag:
					print('[ERROR] Sensor: {} does not measure {}'.format(quadruplet[2],quadruplet[1]))
					exit_flag = True
				if not valid_subsystem_flag:
					print('[ERROR] Subsystem: {} does not contain any sensors that measure {}'.format(quadruplet[3],quadruplet[1]))
					exit_flag = True
	if args.ontology:
		for pair in args.ontology:
			if pair[0] not in nodes_dict:
				print('[ERROR] Node: {} does not exist in nodes.csv'.format(quadruplet[0]))
				exit_flag = True
			if pair[1] not in ontology_dict:
				print('[ERROR] Ontology: {} does not exist in sensors.csv'.format(pair[1]))
	if exit_flag:
		exit(1)

	node_list = []
	triplet_list = []
	node_to_triplet_dict = {}
	triplet_to_node_dict = OrderedDict()
	if args.plot:
		for quadruplet in args.plot:
			if quadruplet[0] not in node_list:
				node_list.append(quadruplet[0])
			if quadruplet[0] not in node_to_triplet_dict:
				node_to_triplet_dict[quadruplet[0]] = []
			triplet = (quadruplet[1],quadruplet[2],quadruplet[3])
			if triplet not in triplet_list:
				triplet_list.append(triplet)
			if triplet not in node_to_triplet_dict[quadruplet[0]]:
				node_to_triplet_dict[quadruplet[0]].append(triplet)
			if triplet not in triplet_to_node_dict:
				triplet_to_node_dict[triplet] = []
			if quadruplet[0] not in triplet_to_node_dict[triplet]:
				triplet_to_node_dict[triplet].append(quadruplet[0])

	node_to_ontology_dict = {}
	ontology_to_node_dict = {}
	if args.ontology:
		for pair in args.ontology:
			for triplet in ontology_dict[pair[1]]:
				triplet = tuple(triplet)
				if triplet not in triplet_list:
					triplet_list.append(triplet)
			if pair[0] not in node_list:
				node_list.append(pair[0])
			if pair[0] not in node_to_ontology_dict:
				node_to_ontology_dict[pair[0]] = []
			if pair[1] not in ontology_to_node_dict:
				ontology_to_node_dict[pair[1]] = []
			if pair[1] not in node_to_ontology_dict[pair[0]]:
				node_to_ontology_dict[pair[0]].append(pair[1])
			if pair[0] not in ontology_to_node_dict[pair[1]]:
				ontology_to_node_dict[pair[1]].append(pair[0])

	and_pattern_list = []
	for triplet in triplet_list:
		pattern = '{}.*{}.*{}'.format(triplet[2],triplet[1],triplet[0])
		and_pattern_list.append(pattern)

	ylabel_list = []
	for triplet in triplet_list:
		if triplet_to_hrf_unit_dict[triplet] not in ylabel_list:
			ylabel_list.append(triplet_to_hrf_unit_dict[triplet])
	
	if (len(ylabel_list) > 2 and args.overlay) or (len(ylabel_list) > 2 and not args.overlay and args.layout == [1,1]):
		print('[ERROR] Cannot overlay data with more than 2 different units on one plot')
		exit(1)

	input_path = datacsv_path

	# determine which column the data is in
	data_column = 0
	header_list = ['value_hrf','value_hrf_average','value_hrf_moving_average']
	with open(input_path,'r') as f:
		header = f.readline()
		header = header.strip().split(',')
		for string in header_list:
			if string in header:
				data_column = header.index(string) + 1

	temp_data_path = os.path.join(data_directory,'scratch')
	if not os.path.exists(temp_data_path):
		os.makedirs(temp_data_path)

	# determine how many days long the time frame is
	time_list = args.timeframe[0].split('-')
	for i,item in enumerate(time_list):
		time_list[i] = int(item)
	timeframe_start = datetime.date(time_list[0],time_list[1],time_list[2])
	time_list = args.timeframe[1].split('-')
	for i,item in enumerate(time_list):
		time_list[i] = int(item)
	timeframe_end = datetime.date(time_list[0],time_list[1],time_list[2])
	timeframe_end = timeframe_end+datetime.timedelta(1)
	timeframe = (timeframe_end-timeframe_start).days


	date_list = []
	for i in range(timeframe):
		date_list.append((timeframe_start+datetime.timedelta(i)).strftime("%Y/%m/%d"))


	# first extract data for every date in the timeframe that doesn't
	# have data yet into a temp file
	all_date_pattern = ''
	for date in date_list:
		if not os.path.exists(os.path.join(temp_data_path,date.replace('/','-'))):
			all_date_pattern += date if len(all_date_pattern) == 0 else '\\|{}'.format(date)

	temp_extract_path = ''
	if len(all_date_pattern) > 0:
		temp_extract_path = os.path.join(temp_data_path,'temp.csv')
		print('Extracting data for all dates in time frame...')
		grep(all_date_pattern,input_path,temp_extract_path)

	# then extract each day from the temp file
	for date in date_list:
		input_path = temp_extract_path
		dash_date = date.replace('/','-')
		date_directory = os.path.join(temp_data_path,dash_date)
		if not os.path.exists(date_directory):
			os.makedirs(date_directory)
		extract_path = os.path.join(date_directory,'{}.csv'.format(dash_date))
		if not os.path.exists(extract_path):
			print('Extracting data for {}...'.format(date))
			grep(date,temp_extract_path,extract_path)

		# extract data for each node from each day in the timeframe
		# input_path = extract_path
		for node in node_list:
			input_path = os.path.join(date_directory,'{}.csv'.format(dash_date))
			node_directory = os.path.join(date_directory,node)
			if not os.path.exists(node_directory):
				os.makedirs(node_directory)
			extract_path = os.path.join(node_directory,'{}.csv'.format(node))
			if not os.path.exists(extract_path):
				print('Extracting data for node {} on {}...'.format(node,date))
				grep(node,input_path,extract_path)

			# extract data for each parameter, sensor, subsystem triplet
			# input_path = extract_path
			if args.plot and node in node_to_triplet_dict:
				for i,triplet in enumerate(node_to_triplet_dict[node]):
					input_path = os.path.join(node_directory,'{}.csv'.format(node))
					extract_path = os.path.join(node_directory,'{}-{}-{}.csv'.format(triplet[0],triplet[1],triplet[2]))
					if not os.path.exists(extract_path):
						# print('Extracting {} data from node {}...'.format(triplet[0],node))
						grep(and_pattern_list[i],input_path,extract_path,useAnd=True)
						cut(',','1,{}'.format(data_column),extract_path,extract_path)
					if os.stat(extract_path).st_size == 0:
						print('[WARNING] No {} data from sensor {} in subsystem {} for node {} on {} exists'.format(triplet[0],triplet[1],triplet[2],node,date))
						os.unlink(extract_path)
			if args.ontology and node in node_to_ontology_dict:
				for i,triplet in enumerate(ontology_dict[node_to_ontology_dict[node][0]]):
					triplet = tuple(triplet)
					input_path = os.path.join(node_directory,'{}.csv'.format(node))
					extract_path = os.path.join(node_directory,'{}-{}-{}.csv'.format(triplet[0],triplet[1],triplet[2]))
					if not os.path.exists(extract_path):
						print('Extracting {} data from node {}...'.format(triplet[0],node))
						grep(and_pattern_list[i],input_path,extract_path,useAnd=True)
						cut(',','1,{}'.format(data_column),extract_path,extract_path)
					if os.stat(extract_path).st_size == 0:
						print('[WARNING] No {} data from sensor {} in subsystem {} for node {} on {} exists'.format(triplet[0],triplet[1],triplet[2],node,date))
						os.unlink(extract_path)
	if os.path.exists(temp_extract_path):
		os.unlink(temp_extract_path)

	final_data_directory = os.path.join(temp_data_path,'final')
	if not os.path.exists(final_data_directory):
		os.makedirs(final_data_directory)
	clearDir(final_data_directory)

	# combine data for each triplet over the timeframe
	# chronological = list(reversed(date_list))
	if args.plot:
		for node in node_to_triplet_dict:
			for triplet in node_to_triplet_dict[node]:
				print('Combining data for {} {} {} {}'.format(node,triplet[0],triplet[1],triplet[2]))
				final_data_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
				with open(final_data_path,'w+') as f:
					for date in date_list:
						read_path = os.path.join(temp_data_path,date.replace('/','-'),node,'{}-{}-{}.csv'.format(triplet[0],triplet[1],triplet[2]))
						if os.path.exists(read_path):
							with open(read_path,'r') as r:
								f.write(r.read())
				if args.trim:
					trimOutliers(final_data_path)
				if not os.path.exists(final_data_path):
					open(final_data_path, 'a').close()

	if args.ontology:
		for node in node_to_ontology_dict:
			for triplet in ontology_dict[node_to_ontology_dict[node][0]]:
				print('Combining data for {} {} {} {}'.format(node,triplet[0],triplet[1],triplet[2]))
				final_data_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
				with open(final_data_path,'w+') as f:
					for date in date_list:
						read_path = os.path.join(temp_data_path,date.replace('/','-'),node,'{}-{}-{}.csv'.format(triplet[0],triplet[1],triplet[2]))
						if os.path.exists(read_path):
							with open(read_path,'r') as r:
								f.write(r.read())
				if args.trim:
					trimOutliers(final_data_path)
				if not os.path.exists(final_data_path):
					open(final_data_path, 'a').close()

	# create plot directory
	plot_directory = os.path.join(data_directory,'plots')
	if not os.path.exists(plot_directory):
		os.makedirs(plot_directory)

	# find what ontology each triplet is in
	triplet_to_ontology_dict = {}
	for ontology in ontology_dict:
		for triplet in triplet_list:
			if list(triplet) in ontology_dict[ontology]:
				triplet_to_ontology_dict[triplet] = ontology

	# find the min and max value for each ylabel over multiple files
	ylabel_to_min_max_dict = {}
	ylabel_to_values_dict = {}
	for file in os.listdir(final_data_directory):
		file_list = file.replace('.csv','').split('-')
		triplet = (file_list[1],file_list[2],file_list[3])
		ylabel = triplet_to_hrf_unit_dict[triplet]
		file_path = os.path.join(final_data_directory,file)
		min_y = float("inf")
		max_y = 0.0
		data = readDataFile(file_path)
		min_y = data['value_hrf'].min()
		max_y = data['value_hrf'].max()
		if ylabel not in ylabel_to_values_dict:
			ylabel_to_values_dict[ylabel] = [min_y,max_y]
		else:
			ylabel_to_values_dict[ylabel].append(min_y)
			ylabel_to_values_dict[ylabel].append(max_y)
	for ylabel in ylabel_to_values_dict:
		ylabel_to_min_max_dict[ylabel] = (min(ylabel_to_values_dict[ylabel]),max(ylabel_to_values_dict[ylabel]))


	# set the title for the plot
	# node1 | vsn | description | address\nnode2 | vsn | ...\nnode3 ...
	# for multiplots node1 | vsn | description | address for each plot
	title_list = []
	if args.overlay or args.layout == [1,1]:
		title = ''
		for i,node in enumerate(node_list):
			node_info = '{} | {} | {} | {}'.format(node,nodes_dict[node][0],nodes_dict[node][2],nodes_dict[node][1].replace('"',''))
			if i == 0:
				title = node_info
			elif i%3 != 0:
				title = '{} & {}'.format(title,node_info)
			else:
				title = '{}\\n{}'.format(title,node_info)

		title_list.append(title)
	else: # layout is set to something other than 1,1 and over lay is not set (not used)
		if args.plot:
			for node in node_to_triplet_dict:
				for triplet in node_to_triplet_dict[node]:
					title_list.append('{} {}'.format(node,triplet[0]))
		title_list.append('title')

	ylabel = ''
	plot = ''
	tics = 'tics'
	multiplot = ''
	x_range = "['{start}':'{end}']".format(start=start_date,end=end_date)
	time_period = '{} to {}'.format(start_date,end_date)
	logscale = ''
	if args.logscale:
		logscale = 'set logscale y'

	# set the y label and construct plot string
	if len(ylabel_list) == 1 and (args.overlay or args.layout == [1,1]): # simplest plot
		ylabel = 'set ylabel noenhanced "{}"'.format(ylabel_list[0])
		plot = ''
		if args.plot:
			for node in node_to_triplet_dict:
				for triplet in node_to_triplet_dict[node]:
					dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
					if not os.path.exists(dataset_path):
						continue
					elif os.stat(dataset_path).st_size == 0:
						continue
					if len(plot) == 0:
						plot = '{} "{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens}" noenhanced'.format(plot,path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1])
					else:
							plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens}" noenhanced'.format(path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1]))
					# tics = 'tics'

		if args.ontology:
			for node in node_to_ontology_dict:
				for ontology in node_to_ontology_dict[node]:
					for triplet in ontology_dict[ontology]:
						triplet = tuple(triplet)
						dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
						if not os.path.exists(dataset_path):
							continue
						elif os.stat(dataset_path).st_size == 0:
							continue
						if len(plot) == 0:
							plot = '{} "{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens}" noenhanced'.format(plot,path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1])
						else:
								plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens}" noenhanced'.format(path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1]))
		tics = 'tics'

	elif len(ylabel_list) == 2 and (args.overlay or args.layout == [1,1]): # plot overlaid with 2 different y labels
		ylabel = 'set ylabel noenhanced "{}"\nset y2label "{}"'.format(ylabel_list[0],ylabel_list[1])
		plot = ''
		if args.plot:
			for node in node_to_triplet_dict:
				for triplet in node_to_triplet_dict[node]:
					dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
					if not os.path.exists(dataset_path):
						continue
					elif os.stat(dataset_path).st_size == 0:
						continue
					if len(plot) == 0:
						plot = '{} "{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens} ({unit})" noenhanced'.format(plot,path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1],unit=triplet_to_hrf_unit_dict[triplet])
					else:
							plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens} ({unit})" noenhanced'.format(path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1],unit=triplet_to_hrf_unit_dict[triplet]))
					if triplet_to_hrf_unit_dict[triplet] == ylabel_list[1]:
						plot = "{} {}".format(plot, 'axes x1y2')
					tics = 'ytics nomirror autofreq tc lt 1 textcolor "black"\nset y2tics nomirror autofreq tc lt 2 textcolor "black"'
		if args.ontology:
			for node in node_to_ontology_dict:
				for ontology in node_to_ontology_dict[node]:
					for triplet in ontology_dict[ontology]:
						triplet = tuple(triplet)
						dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
						if not os.path.exists(dataset_path):
							continue
						elif os.stat(dataset_path).st_size == 0:
							continue
						if len(plot) == 0:
							plot = '{} "{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens} ({unit})" noenhanced'.format(plot,path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1],unit=triplet_to_hrf_unit_dict[triplet])
						else:
								plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{node} | {ontology} | {param} by sensor {sens} ({unit})" noenhanced'.format(path=dataset_path,node=node,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1],unit=triplet_to_hrf_unit_dict[triplet]))
						if triplet_to_hrf_unit_dict[triplet] == ylabel_list[1]:
							plot = "{} {}".format(plot, 'axes x1y2')
						tics = 'ytics nomirror autofreq tc lt 1 textcolor "black"\nset y2tics nomirror autofreq tc lt 2 textcolor "black"'

	else: # layout is set and overlay is not so... multiplot
		multiplot = ''
		if args.plot:
			for triplet in triplet_to_node_dict:
			# print(triplet_to_node_dict)
				for node in triplet_to_node_dict[triplet]:
					# print(node)
					dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
					unit = triplet_to_hrf_unit_dict[triplet]
					title = 'set title "{} | {} | {} | {}"\n'.format(node,nodes_dict[node][0],nodes_dict[node][2],nodes_dict[node][1].replace('"',''))
					yrange = 'set yrange [{min}:{max}]\n'.format(min=ylabel_to_min_max_dict[unit][0],max=ylabel_to_min_max_dict[unit][1])
					ylabel = 'set ylabel noenhanced "{}"\n'.format(unit)
					plot = 'plot "{path}" using 1:2 with lines title "{ontology} | {param} by sensor {sens}" noenhanced\n'.format(path=dataset_path,ontology=triplet_to_ontology_dict[triplet],param=triplet[0],sens=triplet[1])

					multiplot += title
					multiplot += yrange
					multiplot += ylabel
					multiplot += plot
		if args.ontology:
			for ontology in ontology_to_node_dict:
				for node in ontology_to_node_dict[ontology]:
					title = 'set title "{} | {} | {} | {}"\n'.format(node,nodes_dict[node][0],nodes_dict[node][2],nodes_dict[node][1].replace('"',''))
					plot = ''
					for triplet in ontology_dict[ontology]:
						triplet = tuple(triplet)
						dataset_path = os.path.join(final_data_directory,'{}-{}-{}-{}.csv'.format(node,triplet[0],triplet[1],triplet[2]))
						if len(plot) == 0:
							plot = 'plot "{path}" using 1:2 with lines title "{ontology} | {param} by sensor {sens}" noenhanced'.format(path=dataset_path,ontology=triplet_to_ontology_dict[triplet],node=node,param=triplet[0],sens=triplet[1])
						else:
							plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{ontology} | {param} by sensor {sens}" noenhanced'.format(path=dataset_path,ontology=triplet_to_ontology_dict[triplet],node=node,param=triplet[0],sens=triplet[1]))
						unit = triplet_to_hrf_unit_dict[triplet]
						yrange = 'set yrange [{min}:{max}]\n'.format(min=ylabel_to_min_max_dict[unit][0],max=ylabel_to_min_max_dict[unit][1])
						ylabel = 'set ylabel noenhanced "{}"\n'.format(unit)
					multiplot += title
					multiplot += yrange
					multiplot += ylabel
					if '\n' not in plot:
						plot += '\n'
					multiplot += plot


	# print(tics)

	single_plot_template = '''
reset
set terminal png medium size {resolution} enhanced font "Helvetica,{title_font_size}" #ffffff #000000 #404040 #ff0000 #e41a1c #377eb8 #4daf4a #984ea3 #ff7f00 #ffff33 #a65628 #f781bf #999999
set title "{title}\\n{{/={provenance_font_size} Created: {today}, Data: {data_address}, Code: Version {version} of {{/Courier {code}}}}}\\n{{/={provenance_font_size} Command: {{/Courier python3 {command}}}}}"
set tics font "Helvetica,{plot_font_size}"
set output "{path}/{output}"
set xlabel "Time (UTC)"
set datafile separator ','
set timefmt '%Y/%m/%d %H:%M:%S'
{ylabel}
set xdata time
set autoscale
set xrange {xrange}
{logscale}
set format x "%H.%M\\n%m/%d"
set {tics}
set grid
set key font ",{plot_font_size}"
plot {plot}
'''

	multi_plot_template = '''
reset
set terminal png medium size {resolution} enhanced font "Helvetica,{title_font_size}" #ffffff #000000 #404040 #ff0000 #e41a1c #377eb8 #4daf4a #984ea3 #ff7f00 #ffff33 #a65628 #f781bf #999999
set tics font "Helvetica,{plot_font_size}"
set output "{path}/{output}"
set xlabel "Time (UTC)"
set datafile separator ','
set timefmt '%Y/%m/%d %H:%M:%S'
set xdata time
set format x "%H.%M\\n%m/%d"
set xrange {xrange}
set grid
{logscale}
set key font ",{plot_font_size}"
set multiplot layout {layout} title "{{/={provenance_font_size} Created: {today}, Data: {data_address}, Code: Version {version} of {{/Courier {code}}}}}\\n{{/={provenance_font_size} Command: {{/Courier python3 {command}}}}}"
{multiplot}
unset multiplot
'''
	# set up the command for provenance
	i_string = '-i {} '.format(args.input)
	o_string = '-o {} '.format(args.output) if args.output != 'output.png' else ''
	t_string = '-t {} {} '.format(args.timeframe[0],args.timeframe[1])
	p_string = ''
	if args.plot:
		for quadruplet in args.plot:
			add = '-p {} {} {} {} '.format(quadruplet[0],quadruplet[1],quadruplet[2],quadruplet[3])
			p_string += add
	n_string=''
	if args.ontology:
		for pair in args.ontology:
			add = '-n {} {} '.format(pair[0],pair[1])
			n_string += add
	v_string = '-v ' if args.overlay else ''
	l_string = '-l {} {} '.format(args.layout[0],args.layout[1]) if args.layout != [1,1] else ''
	m_string = '-r ' if args.trim else ''
	s_string = '-s ' if args.logscale else ''
	F_string = '-F {} '.format(args.titlefont[0]) if args.titlefont[0] != 16 else ''
	f_string = '-f {} '.format(args.plotfont[0]) if args.plotfont[0] != 12 else ''
	e_string = '-e {} '.format(args.provenancefont[0]) if args.provenancefont[0] != 14 else ''
	r_string = '-r {} {}'.format(args.resolution[0],args.resolution[1]) if args.resolution != [1920,1080] else ''

	address = args.input if not args.address else args.address
	if '_' in address:
		address = address.replace('_','\\\\_')

	if '_' in i_string:
		i_string = i_string.replace('_','\\\\_')

	if '_' in o_string:
		o_string = o_string.replace('_','\\\\_')

	if '_' in p_string:
		p_string = p_string.replace('_','\\\\_')

	if '_' in n_string:
		n_string = n_string.replace('_','\\\\_')


	context = { # in alphabetical order based on key
		# 'address':address,
		'code':'gen\\\\_custom\\\\_plots.py',
		'command':'gen\\\\_custom\\\\_plots.py {i}{o}{t}{p}{n}{v}{l}{m}{s}{F}{f}{e}{r}'.format(i=i_string,o=o_string,t=t_string,p=p_string,n=n_string,v=v_string,l=l_string,m=m_string,s=s_string,F=F_string,f=f_string,e=e_string,r=r_string),
		# 'description':description,
		'data_address':address,
		'layout':'{},{}'.format(args.layout[0],args.layout[1]),
		'logscale':logscale,
		'multiplot':multiplot,
		'node':node,
		# 'vsn':vsn,
		'ontology':ontology,
		# 'ontology_underscores':ontology.replace('/','_'),
		'output':args.output,
		# 'parameter':'parameter_string',
		'path':plot_directory,
		'plot':plot,
		'plot_font_size':args.plotfont[0],
		'provenance_font_size':args.provenancefont[0],
		'resolution':'{},{}'.format(args.resolution[0],args.resolution[1]),
		# 'sensor':'sensor_string',
		'tics':tics,
		'time_period':time_period,
		'title':title_list[0],
		'title_font_size':args.titlefont[0],
		'today':datetime.datetime.utcnow().strftime("%Y-%m-%d"),
		'version':'1',
		'xrange':x_range,
		'ylabel':ylabel,
	}

	if args.overlay or args.layout == [1,1]:
		output = single_plot_template.format(**context).strip()
	else:
		output = multi_plot_template.format(**context).strip()

	with open('graph.plt','w') as f:
		f.write(output)

	input_string = args.input.strip('/')
	print("Plotting data to {input}/plots/{output}".format(input=input_string,output=args.output))

	subprocess.run(['gnuplot', 'graph.plt'])
	subprocess.run(['rm', 'graph.plt'])
