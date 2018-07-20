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
	output_dir = str(sys.argv[3])
	date = str(sys.argv[4])

	dicts = getNodes(project_dir)
	nodes_dict = dicts[0]

	input_path = os.path.join(input_dir,'data.csv')

	# set up file structure (project_dir/data/node_id/date/date.csv)
	data_dir = os.path.join(output_dir,'data')
	os.makedirs(data_dir,exist_ok=True)
	print('Extracting node data for {}.'.format(date))
	for node in nodes_dict:
		node_dir = os.path.join(data_dir,node)
		os.makedirs(node_dir,exist_ok=True)
		os.makedirs(date_dir,exist_ok=True)

		# extract data for a node
		status = grep(node,input_path,output_path)
