#!/usr/bin/env python3

import collections
import argparse
import sys
import os
import re

parent = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
utils = os.path.join(parent,'utils')
sys.path.append(utils)

from plotting_utilities import getNodes,getSensors

def prettyParams(matchobj):
	out = matchobj.group()
	out = out.upper()
	out_list = list(out)
	for char in out_list:
		if char.isnumeric():
			subscript = '<sub>{}</sub>'.format(char)
			char = subscript
	out = str(out_list)
	return out

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate tables')
	parser.add_argument('project_dir', help='path to the project directory you want to generate tables for')
	args = parser.parse_args()
	
	if not os.path.exists(args.project_dir):
		print('[ERROR] {} does not exist'.format(args.project_dir))

	required_files = ['nodes.csv','sensors.csv']
	exit_flag = False
	for file in required_files:
		file_path = os.path.join(args.project_dir,file)
		if not os.path.exists(file_path):
			print('[ERROR] {} does not exist in the input path'.format(file))
			exit_flag = True
	if exit_flag:
		exit(1)

	cwd = os.getcwd()
	path_prefix = './build'

	dicts = getNodes(args.project_dir)
	nodes_dict = dicts[0]
	details_dict = dicts[1]

	dicts = getSensors(args.project_dir)
	parameter_to_sensor_subsystem_dict = dicts[0]
	ontology_dict = dicts[1]
	subcategory_to_hrf_unit_dict = dicts[2]
	hrf_unit_to_sensor_dict = dicts[3]

	# for key in ontology_dict:
	# 	print('{}:{}'.format(key,ontology_dict[key]))

	tables_path = os.path.join(args.project_dir,'tables')
	if not os.path.exists(tables_path):
		os.makedirs(tables_path)

	header = '''
<html>
<head>
<title>Waggle Sensor Plots</title>
<style>
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
}}
.table td span {{
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: inline-block;
        max-width: 100%;
      }}
</style>
<link rel="stylesheet" href="style.css">
</head>
<body>

<h2>Waggle Sensor Plots for Node {node_id} | {vsn} | {description} | {address} </h2>

<table class="layout display responsive-table">
  <thead>
    <tr>
      <th>Ontology</th>
      <th>Category</th>
      <th>Subcategory</th>
      <th>Parameter</th>
      <th>Sensors</th>
      <th>Subsystem</th>
      <th>Plots</th>
    </tr>
  </thead>
  <tbody>
    '''



	footer = '''
</tbody>
</table>
</body>
</html>
    '''

	template_top = '''
    <tr>
      <td rowspan="{span_top}">{top}</td>
      <td rowspan="{span_mid}">{mid}</td>
      <td rowspan="{span_bot}">{bot}</td>
      <td>{parameter}</td>
      <td>{sensor}</td>
      <td>{subsystem}</td>
      <td>
        {day_link}
	    {week_link}
	    {month_link}
      </td>
    </tr>
    '''

	template_mid = '''
    <tr>
      <td rowspan="{span_mid}">{mid}</td>
      <td rowspan="{span_bot}">{bot}</td>
      <td>{parameter}</td>
      <td>{sensor}</td>
      <td>{subsystem}</td>
      <td>
        {day_link}
	    {week_link}
	    {month_link}
      </td>
    </tr>
    '''

	template_bot = '''
	<tr>
	  <td rowspan="{span_bot}">{bot}</td>
	  <td>{parameter}</td>
	  <td>{sensor}</td>
	  <td>{subsystem}</td>
	  <td>
		{day_link}
	    {week_link}
	    {month_link}
	  </td>
	</tr>
    '''

	template_last = '''
	<tr>
	  <td>{parameter}</td>
	  <td>{sensor}</td>
	  <td>{subsystem}</td>
	  <td>
	    {day_link}
	    {week_link}
	    {month_link}
	  </td>
	</tr>
    '''

# <a href="{path_prefix}/plots/{node_id}/day/{node_id}-{ontology}-day.png">Day</a>
# <a href="{path_prefix}/plots/{node_id}/week/{node_id}-{ontology}-week.png">Week</a>
# <a href="{path_prefix}/plots/{node_id}/month/{node_id}-{ontology}-month.png">Month</a>

	for i,node in enumerate(nodes_dict):

		with open(os.path.join(tables_path,'{}-table.html'.format(node)),'w+') as f:
			short_context = {
				'node_id':node,
				'vsn':nodes_dict[node][0],
				'description':nodes_dict[node][2],
				'address':nodes_dict[node][1]
			}
			header_str = header.format(**short_context)
			f.write(header_str)

			prev_top, prev_mid, prev_bot = '','',''

			audio_count = 0
			for ontology in ontology_dict:
				if 'pm_' in ontology:
					continue
				if 'audio' in ontology and audio_count >= 2:
					continue
				ontology_list = ontology.split('/')
				ontology_list.remove('')
				top = ontology_list[0].capitalize()
				mid = ontology_list[1].replace('_',' ').title()
				bot = ontology_list[2].replace('_',' ').title()
				if len(bot) == 2:
					bot = bot.upper()


				if len(ontology_list) == 4:
					parameter = ontology_list[3]
				ontology_str = ontology.strip('/').replace('/','_')
				# print(ontology_dict[ontology])
				parameter = ''
				sensor = ''
				subsystem = ''
				for triplet in ontology_dict[ontology]:
					if len(sensor) == 0:
						parameter += triplet[0]
						sensor += triplet[1]
						subsystem += triplet[2]
					else:
						if not triplet[0] in parameter:
							parameter += ', {}'.format(triplet[0])
						if not triplet[1] in sensor:
							sensor += ', {}'.format(triplet[1])
						if not triplet[2] in subsystem:
							subsystem += ', {}'.format(triplet[2])
				re.sub('[a-z]*[23][a-z]*',prettyParams,parameter)

				span_top = 1
				span_mid = 1
				span_bot = 1

				if top == 'Sensing':
					span_top = 18

				if mid == 'Air Quality':
					span_mid = 8

				if bot == 'Gases':
					span_bot = 7

				if mid == 'Meteorology':
					span_mid = 3

				if mid == 'Physical':
					span_mid = 7

				if bot == 'Audio':
					span_bot = 1

				if top == 'System':
					span_top = 22

				if mid == 'Edge Processor':
					span_mid = 3

				if mid == 'Environment':
					span_mid = 5

				if mid == 'Node Controller':
					span_mid = 4

				if mid == 'Other':
					span_mid = 6

				if mid == 'Wagman':
					span_mid = 4

				if bot == 'Audio' and audio_count == 0:
					parameter = 'Octave 1-10 Intensity, Octave Total Intensity'
					audio_count += 1

				day_path = '{path_prefix}/plots/{node_id}/day/{node_id}-{ontology}-day.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)
				week_path = '{path_prefix}/plots/{node_id}/week/{node_id}-{ontology}-week.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)
				month_path = '{path_prefix}/plots/{node_id}/month/{node_id}-{ontology}-month.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)

				alt_day = '{path_prefix}/plots/{node_id}-{ontology}-day.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)
				alt_week = '{path_prefix}/plots/{node_id}-{ontology}-week.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)
				alt_month = '{path_prefix}/plots/{node_id}-{ontology}-month.png'.format(path_prefix=path_prefix,node_id=node,ontology=ontology_str)

				if os.path.exists(day_path):
					day_link = '<a href="{}">Day</a>'.format(os.path.relpath(day_path, 'tables'))
				elif os.path.exists(alt_day):
					day_link = '<a href="{}">Day</a>'.format(os.path.relpath(alt_day, 'tables'))
				else:
					day_link = 'Day'

				if os.path.exists(week_path):
					week_link = '<a href="{}">Week</a>'.format(os.path.relpath(week_path, 'tables'))
				elif os.path.exists(alt_week):
					week_link = '<a href="{}">Week</a>'.format(os.path.relpath(alt_week, 'tables'))
				else:
					week_link = 'Week'

				if os.path.exists(day_path):
					month_link = '<a href="{}">Month</a>'.format(os.path.relpath(month_path, 'tables'))
				elif os.path.exists(alt_month):
					month_link = '<a href="{}">Month</a>'.format(os.path.relpath(alt_month, 'tables'))
				else:
					month_link = 'Month'

				context = {
					'top':top,
					'mid':mid,
					'bot':bot,
					'span_top':span_top,
					'span_mid':span_mid,
					'span_bot':span_bot,
					'parameter':parameter,
					'sensor':sensor,
					'subsystem':subsystem,
					'node_id':node,
					'ontology':ontology_str,
					'path_prefix':args.project_dir,
					'day_link':day_link,
					'week_link':week_link,
					'month_link':month_link
				}

				current_top = top
				current_mid = mid
				current_bot = bot

				depth = 3
				if current_bot != prev_bot:
					depth = 2
				if current_mid != prev_mid:
					depth = 1
				if current_top != prev_top:
					depth = 0

				if depth == 0:
					f.write(template_top.format(**context))
				elif depth == 1:
					f.write(template_mid.format(**context))
				elif depth == 2:
					f.write(template_bot.format(**context))
				elif depth == 3:
					f.write(template_last.format(**context))

				prev_top = current_top
				prev_mid = current_mid
				prev_bot = current_bot

			f.write(footer)

	css_path = os.path.join(tables_path,'style.css')
	css = '''
body{
  padding: 1em;
  background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAcAAAAHCAYAAADEUlfTAAAAQElEQVQIW2P89OvDfwYo+PHjJ4zJwMHBzsAIk0SXAKkCS2KTAEu++vQSbizIKGQAl0SXAJkGlsQmAbcT2Shk+wH0sCzAEOZW1AAAAABJRU5ErkJggg==);
}
a{
  color: #739931;
}
.page{
  max-width: 60em;
  margin: 0 auto;
}
table th,
table td{
  text-align: left;
}
table.layout{
  width: 100%;
  border-collapse: collapse;
}
table.display{
  margin: 1em 0;
}
table.display th,
table.display td{
  border: 1px solid #B3BFAA;
  padding: .5em 1em;
}

table.display th{ background: #D5E0CC; }
table.display td{ background: #fff; }

table.responsive-table{
  box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2);
}

@media (max-width: 30em){
    table.responsive-table{
      box-shadow: none;  
    }
    table.responsive-table thead{
      display: none; 
    }
  table.display th,
  table.display td{
    padding: .5em;
  }
    
  table.responsive-table td:nth-child(1):before{
    content: 'Number';
  }
  table.responsive-table td:nth-child(2):before{
    content: 'Name';
  }
  table.responsive-table td:nth-child(1),
  table.responsive-table td:nth-child(2){
    padding-left: 25%;
  }
  table.responsive-table td:nth-child(1):before,
  table.responsive-table td:nth-child(2):before{
    position: absolute;
    left: .5em;
    font-weight: bold;
  }
  
    table.responsive-table tr,
    table.responsive-table td{
        display: block;
    }
    table.responsive-table tr{
        position: relative;
        margin-bottom: 1em;
    box-shadow: 0 1px 10px rgba(0, 0, 0, 0.2);
    }
    table.responsive-table td{
        border-top: none;
    }
    table.responsive-table td.organisationnumber{
        background: #D5E0CC;
        border-top: 1px solid #B3BFAA;
    }
    table.responsive-table td.actions{
        position: absolute;
        top: 0;
        right: 0;
        border: none;
        background: none;
    }
}
'''
	
	with open(css_path, 'w+') as f:
		f.write(css)
