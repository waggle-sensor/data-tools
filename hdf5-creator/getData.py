#----------+----------+---------------+---------------#
#   Useful functions to parse data read from the file
#   Author : Nikhil Garg
#   Email : nikhil.garg@data61.csiro.au
#----------+----------+---------------+---------------#

import six
import os
import sys
import re
import pprint
from time import time
from collections import OrderedDict
from multiprocessing import Pool
import numpy as np
import subprocess as subp
from datetime import datetime, timedelta
import h5py


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from array_of_things import (get_column_names, subset_node_data,
    convert_to_float, str2float)
from array_of_things.readFile import subset_node_subsystem


def make_data_handler(info_dict):
    """
    use recursive function to go through the whole depth of subsys info dictionary
    """
    out = {}
    if 'datasheet' not in info_dict:
        for item in info_dict:
            out[item] = make_data_handler(info_dict[item])
    else:
        out = dict({'data': [], 'tstamp': [],
                    'nanCount': 0, "hasFloat": 0})
    return out


def process_data(dataIn):
    """
    convert the list of data into a numpy array of appropriate type
    """
    if (dataIn["hasFloat"] == 1) and (dataIn["nanCount"] == 0):
        temp = []
        for item in dataIn["data"]:
            if (item != "NA"):
                if isinstance(item, six.string_types) and (re.search('[a-zA-Z]', item) is not None):
                    temp.append(np.nan)
                else:
                    temp.append(item)
            else:
                temp.append(np.nan)
        return np.array(temp, dtype='f4')
    elif dataIn["hasFloat"] == 0:
        if len(dataIn["data"]) == dataIn["nanCount"]:
            out = np.full(shape=(dataIn["nanCount"],), fill_value=np.nan, dtype='f4')
            return out
        else:
            out = np.array(dataIn['data'])
            if isinstance(out[0], (np.unicode_, np.str_)):
                return out.astype(np.bytes_)
            else:
                return out
    elif (dataIn["hasFloat"] == 1) and (dataIn["nanCount"] < len(dataIn["data"])):
        temp = []
        for item in dataIn["data"]:
            if (item != "NA"):
                if isinstance(item, six.string_types) and (re.search('[a-zA-Z]', item) is not None):
                    temp.append(np.nan)
                else:
                    temp.append(item)
            else:
                temp.append(np.nan)
        return np.array(temp, dtype="f4")


def date2num(date_stamp, units):
    """
    convert date stamp into a float using datetime module. It is to reduce dependency on the
    netcdf4 or matplotlib for this set of scripts
    """
    date_fmt = "%Y-%m-%d %H:%M:%S"
    units_split = units.split(" ")
    if units_split[0] == "minutes":
        factor = 1.0 / 60.0
        ref_date = datetime.strptime(units, "%s %s %s" %
            (units_split[0], units_split[1], date_fmt))
    elif units_split[0] == "seconds":
        factor = 1.0
        ref_date = datetime.strptime(units, "%s %s %s" %
            (units_split[0], units_split[1], date_fmt))
    elif units_split[0] == "hours":
        factor = 1.0 / 3600.0
        ref_date = datetime.strptime(units, "%s %s %s" %
            (units_split[0], units_split[1], date_fmt))
    elif units_split[0] == "days":
        factor = 1.0 / 86400.0
        ref_date = datetime.strptime(units, "%s %s %s" %
            (units_split[0], units_split[1], date_fmt))
    else:
        raise ValueError("Incorrect units specified")
    if isinstance(date_stamp, datetime):
        if ref_date <= date_stamp:
            date_num = (date_stamp - ref_date).total_seconds() * factor
        else:
            raise ValueError("Reference date in units is after the requested time stamp")
    else:
        raise TypeError("date_stamp should be of datetime type")
    return date_num


def parse_time_stamp(tstamp, units="minutes since 2017-01-01 00:00:00"):
    """
    convert time stamp tp a float
    """
    return date2num(datetime.strptime(tstamp, "%Y/%m/%d %H:%M:%S"), units)


def get_data(filename, subsys_info):
    """
    store the data into the object
    """
    data_handle = make_data_handler(subsys_info)

    regex_pat = re.compile("[a-z]")
    if os.stat(filename).st_size > 0:
        with open(filename, 'r') as infile:
            for i, row in enumerate(infile, 0):
                row_split = row.strip().split(",")
                if len(row_split) > 0:
                    if (row_split[3] in data_handle) and (row_split[4] in data_handle[row_split[3]]):
                        if 'data' in data_handle[row_split[3]][row_split[4]]:
                            try:
                                if row_split[2] == "alphasense" and row_split[4] == "bins":
                                    out = "NA"
                                else:
                                    out = str2float(row_split[6].replace('\n', ''), regex_pat)
                            except ValueError:
                                print(row_split)
                            if isinstance(out, float):
                                if data_handle[row_split[3]][row_split[4]]['hasFloat'] != 1:
                                    data_handle[row_split[3]][row_split[4]]['hasFloat'] = 1
                                #check if the values are within the limit when they are float
                                if ((not subsys_info[row_split[3]][row_split[4]]['minval'] == "NA") and
                                    (not subsys_info[row_split[3]][row_split[4]]['minval'] == None)):
                                    out = out if out >= subsys_info[row_split[3]][row_split[4]]['minval'] else np.nan
                                if ((out != np.nan and not subsys_info[row_split[3]][row_split[4]]['maxval'] == "NA") and
                                    (out != np.nan and not subsys_info[row_split[3]][row_split[4]]['maxval'] == None)):
                                    out = out if out <= subsys_info[row_split[3]][row_split[4]]['maxval'] else np.nan
                                data_handle[row_split[3]][row_split[4]]['data'].append(out)
                            else:
                                data_handle[row_split[3]][row_split[4]]['data'].append(out)
                            if out == "NA":
                                data_handle[row_split[3]][row_split[4]]['nanCount'] += 1
                            if row_split[0] != "timestamp":
                                data_handle[row_split[3]][row_split[4]]['tstamp'].append(parse_time_stamp(row_split[0]))
                        else:
                            try:
                                if row_split[2] == "alphasense" and row_split[4] == "bins":
                                    out = "NA"
                                else:
                                    out = str2float(row_split[6].replace('\n', ''), regex_pat)
                            except ValueError:
                                print(row_split)
                            if out == "NA":
                                data_handle[row_split[3]][row_split[4]][row_split[5]]['nanCount'] += 1
                            if isinstance(out, float):
                                if data_handle[row_split[3]][row_split[4]][row_split[5]]['hasFloat'] != 1:
                                    data_handle[row_split[3]][row_split[4]][row_split[5]]['hasFloat'] = 1
                                #check if the values are within the limit when they are float
                                if not subsys_info[row_split[3]][row_split[4]][row_split[5]]['minval'] == "NA":
                                    out = out if out >= subsys_info[row_split[3]][row_split[4]][row_split[5]]['minval'] else np.nan
                                if out != np.nan and not subsys_info[row_split[3]][row_split[4]][row_split[5]]['maxval'] == "NA":
                                    out = out if out <= subsys_info[row_split[3]][row_split[4]][row_split[5]]['maxval'] else np.nan
                                data_handle[row_split[3]][row_split[4]][row_split[5]]['data'].append(out)
                            else:
                                data_handle[row_split[3]][row_split[4]][row_split[5]]['data'].append(out)
                            data_handle[row_split[3]][row_split[4]][row_split[5]]['tstamp'].append(parse_time_stamp(row_split[0]))

    return data_handle


def get_data_p(args):
    """
    function to get data using multiprocessing and call get_data function
    """
    out = {}
    subsys = os.path.basename(args[0]).split('.')[0]
    out[subsys] = get_data(args[0], args[1])
    return out


def get_variable_data(filein, parameter, variable, minval, maxval):
    """
    subset file for a variable from the subsystem[parameter] and return the data
    with its time stamps
    """
    with open(filein, 'r') as infile:
        subset_data = []
        for i, row in enumerate(infile, 0):
            row_split = row.strip().split(',')
            if len(row_split) > 0:
                if row_split[3] == parameter and row_split[4] == variable:
                    subset_data.append(row)
    if len(subset_data) == 0:
        raise ValueError("no rows are found for given %s and %s" % (parameter, variable))

    #print(subset_data[2].split(','))
    if len(subset_data) > 10:
        try:
            if len(subset_data[2].split(',')) > 0:
                dummy = float(subset_data[2].split(',')[6])
            if len(subset_data[-1]) > 0:
                dataout = np.core.records.fromarrays([np.zeros(shape=len(subset_data), dtype='f4'),
                    np.zeros(shape=len(subset_data), dtype='f4')],
                    names=("time", "data"))
            else:
                dataout = np.core.records.fromarrays([np.zeros(shape=(len(subset_data)-1,), dtype='f4'),
                    np.zeros(shape=(len(subset_data)-1,), dtype='f4')],
                    names=("time", "data"))
        except ValueError:
            if len(subset_data[-1]) > 0:
                dataout = np.core.records.fromarrays([np.zeros(shape=len(subset_data), dtype='f4'),
                    np.zeros(shape=len(subset_data), dtype='U20')],
                    names=("time", "data"))
            else:
                dataout = np.core.records.fromarrays([np.zeros(shape=(len(subset_data) - 1,), dtype='f4'),
                    np.zeros(shape=(len(subset_data) - 1,), dtype='U20')],
                    names=("time", "data"))

        for i, row in enumerate(subset_data, 0):
            split_row = row.split(',')
            if len(split_row[0]) > 0 and len(split_row[6]) > 0:
                dataout["time"][i] = date2num(datetime.strptime(split_row[0],
                                         "%Y/%m/%d %H:%M:%S"),
                                         units="minutes since 2017-01-01 00:00:00")
                try:
                    dataout["data"][i] = float(split_row[6]) if split_row[6] != "NA" else np.nan
                except ValueError:
                    if isinstance(split_row[6], bytes):
                        dataout["data"][i] = split_row[6].decode("ascii")
                    else:
                        dataout["data"][i] = split_row[6]
                if not isinstance(dataout["data"][0], (np.unicode_, np.str_, np.bytes_)):
                    if not np.isnan(dataout["data"][i]):
                        if minval is not None:
                            dataout["data"][i] = dataout["data"][i] if (dataout["data"][i] >= minval) else np.nan
                        if maxval is not None:
                            dataout["data"][i] = dataout["data"][i] if (dataout["data"][i] <= maxval) else np.nan
        #if all the values are "NA", convert then them to np.nan
        #mask = np.logical_or(np.where(dataout["data"] == "NA", True, False),
        #                    np.where(dataout["data"] == "", True, False))
        mask = get_element_wise_mask(dataout["data"])
        if np.all(mask):
            dataout["data"] = np.zeros(shape=(len(dataout["data"])), dtype=float)
            dataout["data"][:] = np.nan
        else:
            #if some value are na but we have some other values which are valid, then so something else
            try:
                dataout2 = np.core.records.fromarrays([np.zeros(shape=len(dataout["data"]), dtype='f4'),
                    np.zeros(shape=len(dataout["data"]), dtype='f4')],
                    names=("time", "data"))
                temp = np.zeros(shape=(len(dataout["data"])), dtype=float)
                temp[mask] = np.nan
                temp[~mask] = dataout["data"][~mask].astype("float")
                dataout2["data"] = np.copy(temp)
                dataout2["time"] = np.copy(dataout["time"])
                dataout = np.copy(dataout2)
            except ValueError:
                pass
        return dataout
    else:
        return None


if __name__ == "__main__":
    cwd = "/home/gar305/Documents/array_of_things"

    if not os.path.exists(os.path.join(cwd, "node_names.txt")):
        get_column_names(os.path.join(cwd, 'nodes.csv'),
                2, varout="nodes", unique=False)
    if not os.path.exists(os.path.join(cwd, "subsystem_names.txt")):
        get_column_names(os.path.join(cwd, "sensors.csv"),
                2, varout="subsys", unique=True)
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
                row_item = row.strip().split(',')
                row_item = [row_item[i].strip().replace('"','') for i in [0, 3, 4, 5]]
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
                #item_length = np.array([len(item) for item in row_split])
                #if np.all(np.clip(item_length, 0, 1).astype(bool)):
                if row_split[2] not in subsys_info[subsys]:
                    subsys_info[subsys][row_split[2]] = {}
                if row_split[3] not in subsys_info[subsys][row_split[2]]:
                    if '\r\n' in row_split[7]:
                        subsys_info[subsys][row_split[2]][row_split[3]] = dict([("units", row_split[4]),
                                                                                ("minval", convert_to_float(row_split[5], regex_pat)),
                                                                                ("maxval", convert_to_float(row_split[6], regex_pat)),
                                                                                ("datasheet", [7].replace("\r\n",""))])
                    elif '\n' in row_split[7]:
                        subsys_info[subsys][row_split[2]][row_split[3]] = dict([("units", row_split[4]),
                                                                                ("minval", convert_to_float(row_split[5], regex_pat)),
                                                                                ("maxval", convert_to_float(row_split[6], regex_pat)),
                                                                                ("datasheet", row_split[7].replace("\n",""))])


    # node_id = "001e0610ba46"
    # data_file = os.path.join(cwd, 'data.csv')
    # if os.path.exists(os.path.join(os.getcwd(), "node_%s" % node_id[6:])):
    #     if not os.path.isdir(os.path.join(os.getcwd(), "node_%s" % node_id[6:])):
    #         subset_node_subsystem(data_file, node_id)
    # else:
    #     subset_node_subsystem(data_file, node_id)
    # proc = Pool(processes=len(subsys_names))
    # args = [[os.path.join(cwd, 'node_10ba46', "%s.csv" % item), subsys_info[item]] for item in subsys_info]
    # _dataout = proc.map(get_data_p, args)
    # dataout = {}
    # for i in range(len(_dataout)):
    #     for item in _dataout[i]:
    #         dataout[item] = _dataout[i][item]
    # proc.close()
    # proc.terminate()

    #===========================================================================
    # Add the attributes for the variables
    #===========================================================================
    # with h5py.File(os.path.join("aot_chicago_data.h5"), mode='r+') as datafile:
    #     for node in datafile:
    #         if isinstance(datafile[node], h5py.Group):
    #             for subsystem in datafile[node]:
    #                 if subsystem in subsys_info:
    #                     for param in datafile[node][subsystem]:
    #                         if param in subsys_info[subsystem]:
    #                             if isinstance(datafile[node][subsystem][param], h5py.Group):
    #                                 for var in datafile[node][subsystem][param]:
    #                                     if var != "time":
    #                                         for attr in subsys_info[subsystem][param][var]:
    #                                             if attr not in datafile[node][subsystem][param][var].attrs:
    #                                                 datafile[node][subsystem][param][var].attrs[attr] = subsys_info[subsystem][param][var][attr]
    #                             elif isinstance(datafile[node][subsystem][param], h5py.Dataset):
    #                                 for attr in subsys_info[subsystem][param]:
    #                                     if attr not in datafile[node][subsystem][param].attrs:
    #                                         datafile[node][subsystem][param].attrs[attr] = subsys_info[subsystem][param][attr]