#!/usr/bin/env python3
import collections
import subprocess
import pandas
import numpy
import os
import re
from io import StringIO

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))


def getNodes(path):
	# nodes_dict = [node_id:[vsn,address,description]]
	# details_dict = [node_id:[details]]
	details_dict = collections.OrderedDict()
	nodes_dict = collections.OrderedDict()

	# url = 'https://raw.githubusercontent.com/waggle-sensor/beehive-server/newformat/publishing-tools/projects/AoT_Chicago.complete/nodes.csv'
	# df = pandas.read_csv(url)
	nodes_path = os.path.join(path,'nodes.csv')
	df = pandas.read_csv(nodes_path)

	for _, line in df.iterrows():
		nodes_dict[line['node_id']] = [line['vsn'], line['address'], line['description']]

		p = re.compile('[[][CAP]*[]]')
		m = p.search(line['description'])
		details = ''
		if m:
			details = m.group()
			p = re.compile('[|]')
			details = re.sub(r'\[|\]','',details)
		details_dict[line['node_id']] = list(details)

	return nodes_dict, details_dict


def getSensors(path):
	#get 5 dictionaries:
	#parameter_to_sensor_subsystem_dict = {paramter:[sensor,subsystem]}
	#ontology_dict = {ontology:[parameter,sensor,subsystem]} maps ontology to parameter sensor and subsystem
	#subcategory_to_hrf_unit_dict = {subcategory:[hrf_unit]}
	#hrf_unit_to_sensor_dict = {hrf_unit:[sensor]}
	#triplet_to_hrf_unit_dict = {(param,sens,subs):hrf_unit}

	parameter_to_sensor_subsystem_dict = collections.OrderedDict()
	ontology_dict = collections.OrderedDict()
	subcategory_to_hrf_unit_dict = collections.OrderedDict()
	hrf_unit_to_sensor_dict = collections.OrderedDict()
	triplet_to_hrf_unit_dict = {}

	# url = 'https://raw.githubusercontent.com/waggle-sensor/beehive-server/newformat/publishing-tools/projects/AoT_Chicago.complete/sensors.csv'
	# df = pandas.read_csv(url)
	sensors_path = os.path.join(path,'sensors.csv')
	df = pandas.read_csv(sensors_path)

	for _, line in df.iterrows():
		triplet = (line['parameter'], line['sensor'], line['subsystem'])
		triplet_to_hrf_unit_dict[triplet] = line['hrf_unit']

		#skip lines we don't want to plot in the future by searching parameter
		# p = re.compile('atm|^5um|point|^id|bins')
		p = re.compile('^id|bins')
		match = p.search(line['parameter'])
		if match:
			continue
		p = re.compile('port_mode|/id')
		match = p.search(line['ontology'])
		if match:
			continue

		#create parameter dict
		if (line['parameter'] not in parameter_to_sensor_subsystem_dict):
			parameter_to_sensor_subsystem_dict[line['parameter']] = [[line['sensor'], line['subsystem']]]
		else:
			parameter_to_sensor_subsystem_dict[line['parameter']].append([line['sensor'],line['subsystem']])

		#create ontology dict
		if (line['ontology'] not in ontology_dict):
			ontology_dict[line['ontology']] = [[line['parameter'],line['sensor'],line['subsystem']]]
		else:
			ontology_dict[line['ontology']].append([line['parameter'],line['sensor'],line['subsystem']])

		#create subcategory to unit dict
		ontology_list = line['ontology'].split('/')
		if (ontology_list[3] not in subcategory_to_hrf_unit_dict):
			subcategory_to_hrf_unit_dict[ontology_list[3]] = [line[4]]
		else:
			subcategory_to_hrf_unit_dict[ontology_list[3]].append(line[4])

		#create unit to sensor dict
		if (line[4] not in hrf_unit_to_sensor_dict):
			hrf_unit_to_sensor_dict[line[4]] = [line[2]]
		elif (line[2] not in hrf_unit_to_sensor_dict[line[4]]):
			hrf_unit_to_sensor_dict[line[4]].append(line[2])

	return parameter_to_sensor_subsystem_dict, ontology_dict, subcategory_to_hrf_unit_dict, hrf_unit_to_sensor_dict, triplet_to_hrf_unit_dict


def grep(pattern,input_path,output_path,invert=False,useAnd=False):
	if os.path.exists(input_path):
		path = '.'
		if os.path.exists(os.path.join(parent,'extract.sh')):
			path = parent
		p = subprocess.Popen(['{}/extract.sh'.format(path), '-p', pattern, '-i', input_path, '-o', output_path, '-v', str(invert), '-a', str(useAnd)])
		output, _ = p.communicate()
		if p.returncode == 1: # no matches found
			# print("{} not found".format(pattern))
			return 1
		elif p.returncode == 0: # matches found
			return 0
		else: # grep returned with non-zero exit status > 1
			return 2

def cut(delimiter,fields,input_path,output_path):
	if os.path.exists(input_path):
		path = '.'
		if os.path.exists(os.path.join(parent,'cut.sh')):
			path = parent
		p = subprocess.Popen(['{}/cut.sh'.format(path), '-d', delimiter, '-f', fields, '-i', input_path, '-o', output_path])
		output, _ = p.communicate()
		if p.returncode == 0: # All input files were output successfully. (cut was succesful)
			return 1
		elif p.returncode > 0: # An error occured
			return 0

def readFile(path):
	with open(path, 'r') as file:
		return file.read()


def readDataFile(path):
	csvdata = StringIO(readFile(path))

	if 'value_hrf' not in csvdata.readline():
		names = ['timestamp', 'value_hrf']
	else:
		names = None

	csvdata.seek(0)

	return pandas.read_csv(csvdata, names=names)

def trimOutliers(path):
	data = readDataFile(path)
	length = data.shape[0]
	mean = data['value_hrf'].mean()
	std = data['value_hrf'].std()

	data = data[numpy.abs(data.value_hrf-mean)<=(3*std)] #delete rows not within +-3 standard deviations
	length_new = data.shape[0]
	outliers = length-length_new

	data.to_csv(path,index=False)
	delFirstLine(path)
	return outliers


def delFirstLine(path):
	with open(path, 'r') as fin:
		data = fin.read().splitlines(True)
	with open(path, 'w') as fout:
		fout.writelines(data[1:])

def cleanupEmptyFilesInDir(path):
	for data_file in os.listdir(path):
		data_file_path = os.path.join(path,data_file)
		try:
			if os.path.isfile(data_file_path) and os.stat(data_file_path).st_size <= 56:
				os.unlink(data_file_path)
				#elif os.path.isdir(data_file_path): shutil.rmtree(data_file_path)
		except Exception as e:
			print(e)

def clearDir(path):
	for data_file in os.listdir(path):
		data_file_path = os.path.join(path,data_file)
		try:
			if os.path.isfile(data_file_path):
				os.unlink(data_file_path)
			#elif os.path.isdir(data_file_path): shutil.rmtree(data_file_path)
		except Exception as e:
			print(e)

def getStartDate(path):
	first2lines = subprocess.check_output(['head', '-2', path])
	first2lines = first2lines.decode().split('\n')
	date = first2lines[1].split(',')
	return date[0]


def getEndDate(path):
	last_line = subprocess.check_output(['tail','-1',path])
	last_line = last_line.decode().split(',')
	date = last_line[0]
	return date


if __name__ == '__main__':
	cwd = os.getcwd()
	print(getNodes(cwd))
	print(getSensors(cwd))
