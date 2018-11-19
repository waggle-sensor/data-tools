# Main function to convert the csv file to a HDF5 file
# where the file has following hierarchy
#   Node
#      |__subsystem
#                 |__sensor
#                         |__variable
#
# Written by : Nikhil Garg
# Email : nikhil.garg@data61.csiro.au
# Date : 28 June 2018

from __future__ import print_function
import os
import sys
import six
import re
import pprint
import shutil
import tarfile
import requests
from bs4 import BeautifulSoup
from glob import glob
from datetime import datetime
import subprocess as subp
from collections import OrderedDict
from copy import deepcopy
from multiprocessing import Pool, Process
import h5py
import numpy as np
from netCDF4 import date2num
from argparse import ArgumentParser


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from array_of_things import (get_column_names, subset_node_data, convert_to_float, printFunction)
from array_of_things.readFile import subset_node_subsystem
from array_of_things.getData import get_data_p, get_variable_data, process_data


def get_element_wise_mask(inarr):
    mask = np.zeros(shape=len(inarr), dtype=int)
    for i in range(len(inarr)):
        if inarr[i] == "NA" or inarr[i] == "":
            mask[i] = 1
    return mask.astype(bool)


def check_tar_file(city='Chicago'):
    '''
    download a latest tar file for the specified city to get the latest list of nodes
    '''
    page = requests.get("https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php")
    if page.status_code == 200:
        file_name = None
        file_path = None
        content = BeautifulSoup(page.content, 'html.parser')
        for item in content.contents:
            if hasattr(item, 'contents') and isinstance(item.contents, list) and len(item.contents) >= 1:
                if (city in item.contents[0] and 'complete.recent' in item.contents[0]
                    and 'tar' in item.contents[0]):
                    file_name = item.contents[0]
                    file_path = item.attrs['href']
        if file_name is None or file_path is None:
            raise ValueError("File for %s not found on the webpage" % city)
        else:
            new_file = requests.get(file_path, allow_redirects=True)
            if new_file.status_code != 200:
                raise ValueError("Unable to get the %s from %s url" % (file_name, file_path))
            else:
                if os.path.isfile(os.path.join(os.getcwd(), file_name)):
                    os.remove(os.path.join(os.getcwd(), file_name))
                with open(os.path.join(os.getcwd(), file_name), 'wb') as outfile:
                    outfile.write(new_file.content)
                tar_obj = tarfile.TarFile(os.path.join(os.getcwd(), file_name))
                tar_obj.getmembers()
                node_file_name = None
                for item in tar_obj.members:
                    if 'nodes.csv' in item.name:
                        node_file_name = item.name
                if node_file_name is None:
                    raise RuntimeError('nodes.csv not present in the tarfile')
                    tar_obj.close()
                else:
                    node_file_obj = tar_obj.extractfile(node_file_name)
                    if os.path.isfile(os.path.join(os.getcwd(), 'nodes.csv')):
                        os.remove(os.path.join(os.getcwd(), 'nodes.csv'))
                    with open(os.path.join(os.getcwd(), 'nodes.csv'), 'wb') as outfile:
                        outfile.write(node_file_obj.read())
                    tar_obj.close()
    else:
        raise ValueError("Unable to request the webpage")


def file_writer(cwd, fileIn, fileOut):
    '''
    file writer function which does all the heavy lifting of extracting, reading and
    writing of a hdf5 file
    '''
#    cwd = "/flush1/gar305/aot"

    if not os.path.exists(os.path.join(cwd, "node_names.txt")):
        get_column_names(os.path.join(cwd, 'nodes.csv'), 1, varout="nodes", unique=False)
    if not os.path.exists(os.path.join(cwd, "subsystem_names.txt")):
        get_column_names(os.path.join(cwd, "sensors.csv"), 2, varout="subsys", unique=True)
    #------+------------------+----------------+--------------------#
    # First get the information for each of the nodes from nodes.csv
    #------+------------------+----------------+--------------------#

    node_info = OrderedDict()
    with open(os.path.join(cwd, 'nodes.csv'), 'r') as infile:
        node_info["node_id"] = []
        node_info["address"] = []
        node_info["lon"] = []
        node_info["lat"] = []
        for i, row in enumerate(infile, 0):
            if i > 0:
                if 'Chicago, IL' in row:
                    row = row.replace('Chicago, IL', 'Chicago IL')
                elif 'UChicago, Regenstine' in row:
                    row = row.replace('UChicago, Regenstine', 'UChicago Regenstine')
                elif 'Ave, Chicago' in row:
                    row = row.replace('Ave, Chicago', 'Ave Chicago IL')
                row_item = row.strip().split(',')
                row_item = [row_item[i].strip().replace('"', '') for i in [0, 3, 4, 5]]
                row_item = [item.replace(' ', '_') for item in row_item]
                node_info['lat'].append(float(row_item[2]))
                node_info["lon"].append(float(row_item[3]))
                node_info['node_id'].append(row_item[0][6:])
                node_info["address"].append(row_item[1])

    for item in node_info:
        node_info[item] = np.array(node_info[item])

    node_dir_name = OrderedDict()

    with open(os.path.join(cwd, "node_names.txt"), 'r') as infile:
        for i, item in enumerate(infile, 0):
            if six.PY2:
                if item[6:-1] not in node_dir_name:
                    node_dir_name[item[6:-1]] = item[:-1]
            else:
                if item[6:-1] not in node_dir_name:
                    node_dir_name[item[6:-1]] = item[:-1]

    subsys_names = []
    with open(os.path.join(cwd, "subsystem_names.txt"), "r") as infile:
        for i, item in enumerate(infile, 0):
            if six.PY2:
                subsys_names.append(item[:-1])
            else:
                subsys_names.append(item[:-1])

    node_list = [os.path.join(cwd, "node_%s" % item) for item in node_info["node_id"]]
    node_idx = OrderedDict()

    for item in node_list:
        node_id = os.path.basename(item).split("_")[1]
        idx = int(np.argwhere(node_info['node_id'] == node_id).flatten())
        if six.PY2:
            node_idx[node_id] = dict([("id", idx),
                                      ("address", node_info["address"][idx].astype(str)),
                                      ("lon", node_info["lon"][idx]),
                                      ("lat", node_info["lat"][idx])])
        else:
            node_idx[node_id] = dict([("id", idx),
                                      ("address", node_info["address"][idx]),
                                      ("lon", node_info["lon"][idx]),
                                      ("lat", node_info["lat"][idx])])

    pp = pprint.PrettyPrinter(indent=4)
    regex_pat = re.compile("[a-z]")
    #------+------------------+----------------+-----------------------#
    # Now get the information for each of the sensors on the subsystems
    #------+------------------+----------------+-----------------------#
    subsys_info = OrderedDict()
    for subsys in subsys_names:
        if not os.path.isfile(os.path.join(cwd, "%s_descr.csv" % subsys)):
            subset_node_data(os.path.join(cwd, "sensors.csv"), subsys)
        subsys_info[subsys] = {}
        with open(os.path.join(cwd, "%s_descr.csv" % subsys), 'r') as infile:
            for i, row in enumerate(infile, 0):
                row_split = row.split(',')
                if row_split[2] not in subsys_info[subsys]:
                    subsys_info[subsys][row_split[2]] = {}
                if row_split[3] not in subsys_info[subsys][row_split[2]]:
                    if '\r\n' in row_split[7]:
                        subsys_info[subsys][row_split[2]][row_split[3]] = dict([("units", row_split[4]),
                                                    ("minval", convert_to_float(row_split[5], regex_pat)),
                                                    ("maxval", convert_to_float(row_split[6], regex_pat)),
                                                    ("datasheet", [7].replace("\r\n", "")),
                                                    ("ontology", row_split[0]),
                                                    ("kind", row_split[0].split('/')[1] if '/' in row_split[0] else "title")])
                    elif '\n' in row_split[7]:
                        subsys_info[subsys][row_split[2]][row_split[3]] = dict([("units", row_split[4]),
                                                    ("minval", convert_to_float(row_split[5], regex_pat)),
                                                    ("maxval", convert_to_float(row_split[6], regex_pat)),
                                                    ("datasheet", row_split[7].replace("\n", "")),
                                                    ("ontology", row_split[0]),
                                                    ("kind", row_split[0].split('/')[1] if '/' in row_split[0] else "title")])

    # pp.pprint(subsys_info)


    #this is a slightly more sensible way of opening file and
    #not doing things that have already been done.

    #open a file in write mode, if it doesn't exist, else open in read (edit) mode

    if not os.path.isfile(fileOut):
        fileout = h5py.File(fileOut, mode="w")
        _new_node_list = deepcopy(node_idx)
    else:
        fileout = h5py.File(fileOut, mode="r+")

        #now check if the nodes that have already been processed and stored in the file
        #have a flag completed with value equal to 1 else will have to process that node
        _new_node_list = []
        for item in node_idx:
            if ("node_%s" % item) in fileout and isinstance(fileout["node_%s" % item], h5py.Group):
                if fileout["node_%s" % item].attrs["completed"] == 0:
                    _new_node_list.append(item)
                    del(fileout["node_%s" % item])
            else:
                _new_node_list.append(item)

    node_grp = {}
    subsys_grp = {}
    parameter_grp = {}
    parameter_vars = {}

    for count, item in enumerate(_new_node_list, 0):
        printFunction("Working on node %s %s" % (item, node_dir_name[item]))
        if (not os.path.exists(os.path.join(cwd, "node_%s" % item)) and
            not os.path.isdir(os.path.join(cwd, "node_%s" % item))):
            os.mkdir(os.path.join(cwd, "node_%s" % item))

        if os.path.exists(os.path.join(cwd, "node_%s" % item)):
            count_flag = []
            for _sub_sys in subsys_names:
                if os.path.exists(os.path.join(cwd, "node_%s" % item, "%s.csv" % _sub_sys)):
                    count_flag.append(1)
                else:
                    count_flag.append(0)
            if len(count_flag) > sum(count_flag):
                #subset_node_subsystem_old(os.path.join(cwd, "data.csv"), node_dir_name[item], subsys_names)
                subset_node_subsystem(fileIn, node_dir_name[item])

        for _sub_sys in subsys_names:
            if not os.path.exists(os.path.join(cwd, "node_%s" % item, "%s.csv" % _sub_sys)):
                raise ValueError("Subprocess command didnt work properly")

        node_grp[item] = fileout.create_group("node_%s" % item)
        for _item in node_idx[item]:
            if _item != "id":
                node_grp[item].attrs[_item] = node_idx[item][_item].tolist()
        #create a flag completed and set it to 0
        node_grp[item].attrs["completed"] = 0

        subsys_grp[item] = {}
        parameter_grp[item] = {}
        parameter_vars[item] = {}

        #get the data for all the subsystem using python multiprocessing
        pool_args = [[os.path.join(cwd, 'node_%s' % item, "%s.csv" % _item),
            subsys_info[_item]] for _item in subsys_info]
        #create a pool of threads
        with Pool(processes=len(subsys_names)) as pool:
            #map the arguments to the pool of threads
            _node_subsys_data = pool.map(get_data_p, pool_args)
        node_subsys_data = {}
        for i in range(len(subsys_names)):
            for _item in _node_subsys_data[i]:
                node_subsys_data[_item] = _node_subsys_data[i][_item]

        for subsys in subsys_names:
            if os.path.isfile(os.path.join(cwd, "node_%s" % item, "%s.csv" % subsys)):
                #create subsystem group if the size of file for the subsystem within each node
                #is not 0
                if os.stat(os.path.join(cwd, "node_%s" % item, "%s.csv" % subsys)).st_size > 10:
                    subsys_grp[item][subsys] = node_grp[item].create_group(subsys)
                    parameter_grp[item][subsys] = {}
                    parameter_vars[item][subsys] = {}
                    for param in subsys_info[subsys]:
                        #get_list_of_parameters(os.path.join(cwd, "node_%s" % item, "%s.csv" % subsys), 4):
                        #create parameter group for each subsystem. Do not create parameter if it is
                        #same as subsystem
                        if subsys != param:
                            parameter_grp[item][subsys][param] = subsys_grp[item][subsys].create_group(param)
                            parameter_vars[item][subsys][param] = {}
                            #now create the rest of the variables for the sensor
                            for var in subsys_info[subsys][param]:
                                #get the data for a variable from a specific sensor of a given subsystem mounted
                                #on a node
                                if len(node_subsys_data[subsys][param][var]['data']) > 0:
                                    if "time" not in parameter_vars[item][subsys][param]:
                                        #create time variable for the sensor
                                        #printFunction(var_data["time"][0], type(var_data["time"][0]))
                                        if 'tstamp' in node_subsys_data[subsys][param]:
                                            parameter_vars[item][subsys][param]["time"] = parameter_grp[item][subsys][param].create_dataset("time",
                                                data=np.array(node_subsys_data[subsys][param]["tstamp"][:], dtype='f4'),
                                                dtype='f4', compression="gzip", compression_opts=5)
                                        elif 'tstamp' in node_subsys_data[subsys][param][var]:
                                            parameter_vars[item][subsys][param]["time"] = parameter_grp[item][subsys][param].create_dataset("time",
                                                data=np.array(node_subsys_data[subsys][param][var]["tstamp"][:], dtype='f4'),
                                                dtype='f4', compression="gzip", compression_opts=5)
                                        parameter_vars[item][subsys][param]["time"].dims[0].label = "time"
                                        parameter_vars[item][subsys][param]["time"].attrs["name"] = "utc_timestamp"
                                        parameter_vars[item][subsys][param]["time"].attrs["units"] = "minutes since 2017-01-01 00:00:00"
                                        parameter_vars[item][subsys][param]["time"].attrs["calendar"] = "proleptic_gregorian"
                                    if 'data' in node_subsys_data[subsys][param][var]:
                                        _out_data = process_data(node_subsys_data[subsys][param][var])
                                    elif "data" in node_subsys_data[subsys][param]:
                                        _out_data = process_data(node_subsys_data[subsys][param])
                                    parameter_vars[item][subsys][param][var] = parameter_grp[item][subsys][param].create_dataset(var,
                                                                        data=_out_data, dtype=str(_out_data.dtype),
                                                                        compression="gzip", compression_opts=5)
                                    for attr in subsys_info[subsys][param][var]:
                                        if attr in ["minval", "maxval"]:
                                            if subsys_info[subsys][param][var][attr] is None:
                                                parameter_vars[item][subsys][param][var].attrs[attr] = "None"
                                            else:
                                                parameter_vars[item][subsys][param][var].attrs[attr] = subsys_info[subsys][param][var][attr]
                                        else:
                                            parameter_vars[item][subsys][param][var].attrs[attr] = subsys_info[subsys][param][var][attr]

                                    if hasattr(parameter_vars[item][subsys][param][var], "flush"):
                                        parameter_vars[item][subsys][param][var].flush()
        fileout.flush()
        printFunction("removing directory node_%s " % item)
        shutil.rmtree(os.path.join(cwd, "node_%s" % item))
        #change the value of flag completed to 1
        node_grp[item].attrs["completed"] = 1
        del(node_subsys_data)
        del(_node_subsys_data)
        if '_out_data' in locals() or '_out_data' in globals():
            del(_out_data)
    fileout.attrs[six.u("Created_by")] = six.u("Nikhil Garg")
    fileout.attrs[six.u("Email_address")] = six.u("nikhil.garg@data61.csiro.au")
    fileout.attrs[six.u("Created_on")] = six.u(datetime.utcnow().ctime() + " UTC")
    fileout.attrs[six.u("Description")] = six.u("Data collected from Array of things sensors installed in Chicago. \n"+
                                                "This dataset is freely provided by Argonne National lab on their website \n"+
                                                "https://aot-file-browser.plenar.io/aot-chicago-complete. \n"+
                                                "Due to the large size of datafile, only a subset of data of approximately \n"+
                                                "1GB size was extracted and converted to HDF5. \n"+
                                                "No modification of dataset has been carried out.")

    fileout.close()


if __name__ == "__main__":
    working_directory = "/home/gar305/Documents/array_of_things"
    fileIn = os.path.join(working_directory, "AoT_Chicago.complete.recent.csv")
    fileOut = os.path.join(working_directory, "aot_chicago_data.h5")
    check_tar_file(city='Chicago')
    file_writer(working_directory, fileIn, fileOut)