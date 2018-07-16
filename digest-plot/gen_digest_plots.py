#!/usr/bin/env python3

import collections
import subprocess
import datetime
import requests
import shutil
import pandas
import numpy
import copy
import sys
import re
import os

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
utils = os.path.join(parent,'utils')
sys.path.append(utils)

from plotting_utilities import *

def extractData(input_path,output_path,parameter,sensor,subsystem):
	outliers = 0

	pattern = '{}.*{}'.format(subsystem,sensor)
	status = grep(pattern,input_path,output_path,useAnd=True)
	if status > 0: # grep failed for some reason
		if os.path.exists(output_path):
			os.unlink(output_path)
		return

	cut(',','1,{}'.format(data_column),output_path,output_path)

	outliers = trimOutliers(output_path)
	# delFirstLine(output_path)

	return outliers

def getDates(days=1):
	date_list = []
	for i in range(1,days+1):
		date_list.append((datetime.datetime.utcnow()-datetime.timedelta(i)).strftime("%Y-%m-%d"))
	return date_list

if __name__ == '__main__':
	project_dir = sys.argv[1]
	data_column = sys.argv[2]
	cwd = os.getcwd()

	dicts = getNodes(project_dir)
	nodes_dict = dicts[0]
	details_dict = dicts[1]

	dicts = getSensors(project_dir)
	parameter_to_sensor_subsystem_dict = dicts[0]
	ontology_dict = dicts[1]
	subcategory_to_hrf_unit_dict = dicts[2]
	hrf_unit_to_sensor_dict = dicts[3]

	date_list = getDates(30)

	deleted_old_data = False

	# extract ontology/parameter data from daily data sets
	no_data_nodes = []
	for node in nodes_dict:

		# check if the node has anby data, if it doesn't then delete it from nodes dict later
		path = '{project_dir}/data/{node}'.format(project_dir=project_dir,node=node)
		# if a node has no data, skip it
		if not os.path.exists(path):
			no_data_nodes.append(node)
			continue

		# get details for the node to avoid extraneous operations
		details_dict_verbose = {'C':'chemsense','A':'alphasense','P':'plantower'}
		details = details_dict[node]
		for i,item in enumerate(details):
			details[i] = details_dict_verbose[item]

		# iterate over every date for which data exists
		for file in os.listdir(path):
			if file == 'final':
				continue
			print('Extracting {}/{}...'.format(node,file))

			input_path = os.path.join(path,file,'{}.csv'.format(file))

			outlier_dict = {}

			# iterate over every parameter from sensors.csv
			for parameter in parameter_to_sensor_subsystem_dict:
				input_path = os.path.join(path,file,'{}.csv'.format(file))	

				# get the sensors and subsystems associated with the parameter
				sensor_list = []
				subsystem_list = []
				for value in parameter_to_sensor_subsystem_dict[parameter]:

					sensor_list.append(value[0])
					subsystem_list.append(value[1])

				if (len(sensor_list) == 0 or len(subsystem_list) == 0):
					continue

				# extract just the parameter data from each day
				output_path = '{project_dir}/data/{node}/{file}/{parameter}.csv'.format(project_dir=project_dir,node=node,parameter=parameter,file=file)
				# # if the data has already been extracted, don't do it again
				# if os.path.exists(output_path) or (deleted_old_data and file != datetime.datetime.utcnow().strftime("%Y-%m-%d")):
				# 	continue
				# if not os.path.isfile(output_path):
				# 	with open(output_path,'w+') as f:
				# 		f.close()
				
				status = grep(parameter,input_path,output_path)
				if status > 0:
					continue

				input_path = output_path

				# extract data for each sensor individually
				for i,sensor in enumerate(sensor_list):
					
					subsystem = subsystem_list[i]

					output_path = '{project_dir}/data/{node}/{file}/{parameter}-{sensor}-{subsystem}.csv'.format(project_dir=project_dir,node=node,file=file,sensor=sensor,parameter=parameter,subsystem=subsystem)
					# again, if the data has already been extracted, don't do it again
					if os.path.exists(output_path) or (deleted_old_data and file != datetime.datetime.utcnow().strftime("%Y-%m-%d")):
						continue
					outliers = extractData(input_path,output_path,parameter,sensor,subsystem)
					outlier_dict[parameter] = outliers



			# remove any empty files or files with only headers
			sub_path = os.path.join(path,file)
			for data_file in os.listdir(sub_path):
				p = re.compile('-')
				m = p.search(data_file)
				if not m:
					continue
				data_file_path = os.path.join(sub_path,data_file)

				try:
					if os.path.isfile(data_file_path) and os.stat(data_file_path).st_size <= 56:
						os.unlink(data_file_path)
					#elif os.path.isdir(data_file_path): shutil.rmtree(data_file_path)
				except Exception as e:
					print(e)
	# remove nodes from nodes_dict for which no data exists
	for node in no_data_nodes:
		del nodes_dict[node]




	time_periods = collections.OrderedDict([('day',1),('week',7),('month',30)])

	# combine files for plotting
	for node in nodes_dict:

		path = '{project_dir}/data/{node}'.format(project_dir=project_dir,node=node)
		final_path = os.path.join(path,'final')
		if not os.path.exists(final_path):
			os.makedirs(final_path)

		details_dict_verbose = {'C':'chemsense','A':'alphasense','P':'plantower'}
		details = details_dict[node]

		for time_period in time_periods:
			print('Combining data for {node} for the last {time}...'.format(node=node,time=time_period))
			time_period_path = os.path.join(final_path,time_period)
			if not os.path.exists(time_period_path):
				os.makedirs(time_period_path)

			# if old data was deleted then files to to be recombined, and i don't want to delete the first day of every
			# single file then append the most recent day because combining them doesn't take very long.
			if deleted_old_data:
				clearDir(time_period_path)
			
			for file in os.listdir(time_period_path):
				file_path = os.path.join(time_period_path,file)
				if os.path.exists(file_path) and os.stat(file_path).st_size > 56:
					# print(file_path)
					start_date = getStartDate(file_path)
					datecutoff = (datetime.datetime.utcnow()-datetime.timedelta(time_periods[time_period]-1)).strftime("%Y/%m/%d 00:00:00")
					# print(start_date,datecutoff)
					if start_date < datecutoff:
						# print('deleting...')
						if os.path.exists(file_path):
							os.unlink(file_path)


			date_list = getDates(time_periods[time_period])
			chronological = list(reversed(date_list))

			sensor_list = []
			subsystem_list = []

			for parameter in parameter_to_sensor_subsystem_dict:

				for pair in parameter_to_sensor_subsystem_dict[parameter]:

					sensor_list.append(pair[0])
					subsystem_list.append(pair[1])

				if (len(sensor_list) == 0 or len(subsystem_list) == 0):
					continue

				for i,sensor in enumerate(sensor_list):
					subsystem = subsystem_list[i]
					param_sens_subs = '{}-{}-{}'.format(parameter,sensor,subsystem)

					time_period_data_path = '{path}/{string}-{time}.csv'.format(path=time_period_path,string=param_sens_subs,time=time_period)
					if os.path.exists(time_period_data_path):
						continue

					with open(time_period_data_path,'w+') as f:
						for date in chronological:
							day_path = '{data}/{date}/{string}.csv'.format(data=path,date=date,string=param_sens_subs)
							# print(day_path)
							if os.path.exists(day_path):

								with open(day_path,'r') as r:
									f.write(r.read())

			#delete empty files in each time period
			cleanupEmptyFilesInDir(time_period_path)

		# delete any empty files that somehow ended up in the final folder
		cleanupEmptyFilesInDir(final_path)
		

	# plot generation
	plots_path = '{project_dir}/plots'.format(project_dir=project_dir)
	if not os.path.exists(plots_path):
		os.makedirs(plots_path)

	plot_logs_dir = os.path.join(project_dir,'plot_logs')
	if not os.path.exists(plot_logs_dir):
		os.makedirs(plot_logs_dir)

	removed_dict = {}
	for time_period in time_periods:

		date_list = getDates(time_periods[time_period])
		x_range = "['{start} 00:00:00':'{end} 23:59:59']".format(start=date_list[-1].replace('-','/'),end=date_list[0].replace('-','/'))
		# tomorrow: datetime.date.today()+datetime.timedelta(days=1).strftime()
		for node in nodes_dict:
			with open('{}/{}.log'.format(plot_logs_dir,node),'w+') as f:
				f.write('subsystem,sensor,parameter\n')
			if node not in removed_dict:
				removed_dict[node] = []

			node_plot_path = os.path.join(plots_path,node,time_period)
			if not os.path.exists(node_plot_path):
				os.makedirs(node_plot_path)

			data_path = '{project_dir}/data/{node}/final/{time}'.format(project_dir=project_dir,node=node,time=time_period)		

			vsn = nodes_dict[node][0]
			address = nodes_dict[node][1]
			address = re.sub('"','',address)

			description = nodes_dict[node][2]

			temp_ontology_dict = copy.deepcopy(ontology_dict)

			pm_flag = False

			for ontology in temp_ontology_dict:
				if ontology == '/sensing/air_quality/particulates/pm_2_5' or ontology == '/sensing/air_quality/particulates/pm_10':
					continue
				
				for date in date_list:
					remove = []
					for triplet in temp_ontology_dict[ontology]:
						if not os.path.exists('{data}/{}-{}-{}-{}.csv'.format(triplet[0],triplet[1],triplet[2],time_period,data=data_path)):
							remove.append(triplet)
				for triplet in remove:
					temp_ontology_dict[ontology].remove(triplet)
					removed_dict[node].append(triplet)
					with open('{}/{}.log'.format(plot_logs_dir,node),'a') as f:
						f.write(triplet[2]+','+triplet[1]+','+triplet[0]+'\n')
				if len(temp_ontology_dict[ontology]) == 0:
					# print(ontology)
					continue
				# for key in temp_ontology_dict:
				# 	print(key,temp_ontology_dict[key])
				# print(remove)

				

				ontology_list = ontology.split('/')
				parameter = ontology_list[-1]

				sensor_list = []
				sensor_string = ''
				parameter_list = []
				parameter_string = ''
				plot = ''
				logscale = ''

				# get a list of sensors, parameters and subsytems, as well as 
				# a string for each for the plot
				sensor_list = []
				sensor_set = collections.OrderedDict([])
				sensor_string = ''
				parameter_list = []
				parameter_set = collections.OrderedDict([])
				parameter_string = ''
				subsystem_list = []
				
				for triplet in temp_ontology_dict[ontology]:
					sensor_list.append(triplet[1])
					sensor_set[triplet[1]] = None
					parameter_list.append(triplet[0])
					parameter_set[triplet[0]] = None
					subsystem_list.append(triplet[2])
				for parameter in parameter_set:
					if len(parameter_string) == 0:
						parameter_string = parameter
					else:
						parameter_string = '{}+{}'.format(parameter_string,parameter)
				for sensor in sensor_set:
					if len(sensor_string) == 0:
						sensor_string = sensor
					else:
						sensor_string = '{}+{}'.format(sensor_string,sensor)

				# get labeles for the y axis of each plot
				ylabel_list = []
				for unit in subcategory_to_hrf_unit_dict[ontology_list[3]]:
					if unit not in ylabel_list:
						ylabel_list.append(unit)
						if unit == 'lux' and ontology == '/system/other/light':
							if 'lux' in ylabel_list:
								ylabel_list.remove('lux')
				if 'RH' in ylabel_list:
					for i,item in enumerate(ylabel_list):
						if item == 'RH':
							ylabel_list[i] = '%RH'
				if 'C' in ylabel_list:
					for i,item in enumerate(ylabel_list):
						if item == 'C':
							ylabel_list[i] = 'deg C'


				if ontology_list[-1] == 'particle_count':
					if 'pms7003' in sensor_list:
						# ylabel_list.remove('counts')
						1
					if 'opc_n2' in sensor_list:
						ylabel_list.remove('mg/m^3')

				# if ontology_list[3] == 'pressure':
				# 	ylabel_list.remove('C')

				#plotting pm1, pm2_5, and pm10 on one graph requires a different setup because all 3 have different ontologies
				if ontology_list[-2] == 'particulates' and ontology_list[-1] != 'particle_count':
					sensor_list = []
					sensor_string = ''
					parameter_list = []
					parameter_string = ''
					parameter_set = collections.OrderedDict([])
					subsystem_list = []

					if not pm_flag: 
						pm_flag = True
						pm_list = []
						for ontology in temp_ontology_dict:
							p = re.compile('/sensing/air_quality/particulates/pm_[0125_]*')
							m = p.match(ontology)
							if m:
								pm_list.append(temp_ontology_dict[ontology])
						for triplet in pm_list:
							# print('TRPIPLET',triplet)
							sensor_list.append(triplet[0][1])
							if len(sensor_string) == 0:
								sensor = triplet[0][1]
							else:
								sensor = '{}+{}'.format(sensor,triplet[0][1])
							parameter_list.append(triplet[0][0])
							parameter_set[triplet[0][0]] = None
							subsystem_list.append(triplet[0][2])
						for parameter in parameter_set:
							if len(parameter_string) == 0:
								parameter_string = parameter
							else:
								parameter_string = '{}+{}'.format(parameter_string,parameter)
					ontology = '{}/{}/{}'.format(ontology_list[0],ontology_list[1],ontology_list[2])


				#generate the plot script for plotting only one unit
				if (len(ylabel_list) == 1):
					ylabel = ylabel_list[0]
					plot = ''#"['{start} 00:00:00':'{end} 23:59:59']".format(start=date_list[-1],end=date_list[0])
					
					for i,sensor in enumerate(sensor_list):
						dataset_path = "{dir}/data/{node}/final/{time}/{param}-{sensor}-{subsystem}-{time}.csv".format(dir=project_dir,sensor=sensor,node=node,param=parameter_list[i],subsystem=subsystem_list[i],time=time_period)
						if not os.path.exists(dataset_path):
							continue
						elif os.stat(dataset_path).st_size == 0:
							continue
						if i == 0:
							plot = '{} "{path}" using 1:2 with lines title "{param_upper} by sensor {sensor}"'.format(plot,path=dataset_path,sensor=sensor.replace('_','\\\\_'),param=parameter_list[i].replace('_','\\\\_'),param_upper=parameter_list[i].replace('_','\\\\_'),node=node,subsystem=subsystem_list[i])
						else:
							plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{param_upper} by sensor {sensor}"'.format(path=dataset_path,sensor=sensor.replace('_','\\\\_'),param=parameter_list[i].replace('_','\\\\_'),param_upper=parameter_list[i].replace('_','\\\\_'),node=node,subsystem=subsystem_list[i]))
					tics = 'tics'


				#generate plot script, alternate ylabel and alternate tics for plotting w/ 2 y axes
				elif len(ylabel_list) == 2:
					ylabel = '{}"\nset y2label "{}'.format(ylabel_list[0],ylabel_list[1])
					plot = ''#"['{start} 00:00:00':'{end} 23:59:59']".format(start=date_list[-1],end=date_list[0])
					
					for j,unit in enumerate(ylabel_list):
						for i,sensor in enumerate(sensor_list):
							dataset_path = "{dir}/data/{node}/final/{time}/{param}-{sensor}-{subsystem}-{time}.csv".format(dir=project_dir,sensor=sensor,node=node,param=parameter_list[i],subsystem=subsystem_list[i],time=time_period)
							if sensor not in hrf_unit_to_sensor_dict[unit]:
								continue
							#check if a dataset with data exists
							if  not os.path.exists(dataset_path):
								continue
							elif os.stat(dataset_path) == 0:
								continue

							#add lines to the plot script
							if i == 0:
								plot = '{} "{path}" using 1:2 with lines title "{param_upper} by sensor {sensor} ({unit})" noenhanced'.format(plot,path=dataset_path,sensor=sensor.replace('_','\\\\_'),param=parameter_list[i].replace('_','\\\\_'),param_upper=parameter_list[i].replace('_','\\\\_'),node=node,subsystem=subsystem_list[i],unit=unit)
							else:
								plot = "{}, {}".format(plot,'"{path}" using 1:2 with lines title "{param_upper} by sensor {sensor} ({unit})" noenhanced'.format(path=dataset_path,sensor=sensor.replace('_','\\\\_'),param=parameter_list[i].replace('_','\\\\_'),param_upper=parameter_list[i].replace('_','\\\\_'),node=node,subsystem=subsystem_list[i],unit=unit))
							if (j == 1):
								plot = "{} {}".format(plot, 'axes x1y2')
					tics = 'ytics nomirror autofreq tc lt 1\nset y2tics nomirror autofreq tc lt 2'
					# print(plot,ylabel_list)
							


				# 																	  #background,borders,x,y,plotting....
				plot_template = '''	
set terminal png medium size 1920,1080 enhanced font "Helvetica,16" #ffffff #000000 #404040 #ff0000 #e41a1c #377eb8 #4daf4a #984ea3 #ff7f00 #ffff33 #a65628 #f781bf #999999
set tics font "Helvetica,14"
set output "{path}/{node}-{ontology_underscores}-{time_period}.png"
set title "{vsn} | {description} | {address} | {ontology}\\n{{/*0.7 Created: {today}, Data: {data_address}, Code: Version {version} of {{/Courier {code}}}, Command: {{/Courier ./digest.sh {project}}}}}"
set xlabel "Time (UTC)"
set ylabel noenhanced "{ylabel}"
set datafile separator ','
set timefmt '%Y/%m/%d %H:%M:%S'
set xdata time
set autoscale
set xrange {xrange}
{logscale}
set format x "%H.%M\\n%m/%d"
set {tics}
set grid
plot {plot} 
'''
				

				context = {
					'address':address,
					'code':'gen\\\\_digest\\\\_plots.py',
					'description':description,
					'data_address':project_dir.replace('_','\\\\_').replace('scratch/',''),
					'logscale':logscale,
					'parameter':parameter_string,
					'plot':plot,
					'project':project_dir.replace('_','\\\\_').replace('scratch/',''),
					'node':node,
					'ontology':ontology.replace('_','\\\\_'),
					'ontology_underscores':ontology.strip('/').replace('/','_'),
					'path':node_plot_path,
					'sensor':sensor_string,
					'time_period':time_period,
					'today':datetime.datetime.utcnow().strftime("%Y-%m-%d"),
					'tics':tics,
					'version':'1',
					'vsn':vsn,
					'xrange':x_range,
					'ylabel':ylabel,
				}

				output = plot_template.format(**context).strip()
				# print(output.strip())

				with open('graph.plt','w') as f:
					f.write(output)

				print("Plotting {node} {time_period} {ontology}".format(node=node,time_period=time_period,ontology=ontology))

				subprocess.run(['gnuplot', 'graph.plt'])

	# for key in removed_dict:
	# 	print(key,removed_dict[key])



