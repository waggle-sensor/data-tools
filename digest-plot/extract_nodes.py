#!/usr/bin/env python3

import os
import sys

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
utils = os.path.join(parent,'utils')
sys.path.append(utils)

from plotting_utilities import getNodes, grep

if __name__ == '__main__':
	project_dir = str(sys.argv[1])
	input_dir = str(sys.argv[2])
	date = str(sys.argv[3])

	dicts = getNodes(project_dir)
	nodes_dict = dicts[0]

	input_path = os.path.join(input_dir,'data.csv')

	# set up file structure (project_dir/data/node_id/date/date.csv)
	data_dir = os.path.join(project_dir,'data')
	if not os.path.exists(data_dir):
		os.makedirs(data_dir)
	print('Extracting node data for {}.'.format(date))
	for node in nodes_dict:
		node_dir = os.path.join(data_dir,node)
		if not os.path.exists(node_dir):
			os.makedirs(node_dir)
		date_dir = os.path.join(node_dir,date)
		if not os.path.exists(date_dir):
			os.makedirs(date_dir)
		output_path = os.path.join(date_dir,'{}.csv'.format(date))

		# extract data for a node
		status = grep(node,input_path,output_path)
