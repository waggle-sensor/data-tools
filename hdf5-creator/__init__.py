#-----------+--------------+---------------+----------#
#   A set of python scripts for Array of Things dataset
#   Written by : Nikhil Garg
#   Email : nikhil.garg@data61.csiro.au
#-----------+--------------+---------------+----------#

import os
import six
import sys
import numpy as np
import subprocess as subp
import ctypes


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


if os.uname()[0] == "Darwin":
    LIB_READ_FILE = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.realpath(__file__)), "libreadFile.dylib"))
elif os.uname()[0] == 'Linux':
    LIB_READ_FILE = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(os.path.realpath(__file__)), "libreadFile.so"))


class Arguments(ctypes.Structure):
    """
    class defining the c structure in python
    """
    _fields_ = [("node_names_file", ctypes.c_char_p),
                ("subsystem_name_file", ctypes.c_char_p),
                ("data_file", ctypes.c_char_p),
                ("node_name", ctypes.c_char_p)]


def _readFile(args):
    """
    wrapper function for the C function
    """
    LIB_READ_FILE.readFile.restype = ctypes.c_int
    LIB_READ_FILE.readFile.argtypes = [ctypes.POINTER(Arguments)]
    if isinstance(args, Arguments):
        out = LIB_READ_FILE.readFile(ctypes.byref(args))
    return int(out)


def _subsetFile(args):
    LIB_READ_FILE.subsetFile.restype = ctypes.c_int
    LIB_READ_FILE.readFile.argtypes = [ctypes.c_char_p,
                                       ctypes.c_char_p,
                                       ctypes.c_int]
    out = LIB_READ_FILE.subsetFile(args[0], args[1], args[2])
    return int(out)


def cast_string(inp_string):
    """
    string cast function to handle empty string, python2 and python3
    """
    if len(inp_string) > 0:
        if six.PY2:
            return inp_string
        else:
            return inp_string.encode('utf-8')
    else:
        return ctypes.POINTER(ctypes.c_char_p)()


def subset_node_data(filein, node):
    """
    function to split csv data for the unique nodes or subsystems
    """
    base_path = os.path.dirname(os.path.abspath(filein))
    fileout = os.path.join(base_path, "node_%s.csv" % node[6:])
    _filein = os.path.abspath(filein)
    with open(fileout, 'w') as outfile:
        with open(_filein, 'r') as infile:
            for i, row in enumerate(infile, 0):
                row_split = row.strip().split(',')
                if row_split[1] == node:
                    outfile.write(row)
    return

def get_column_names(filein, col_num, varout="nodes", unique=False):
    """
    function to extract the column names from the file
    """
    if varout == "nodes":
        fileout = os.path.join(os.path.dirname(filein), "node_names.txt")
        with open(fileout, 'w') as outfile:
            row_items = []
            with open(filein, 'r') as infile:
                for i, row in enumerate(infile, 0):
                    if i > 0:
                        row_split = row.strip().split(',')
                        if row_split[col_num] not in row_items:
                            row_items.append(row_split[col_num])
            if len(row_items) > 0:
                for i, item in enumerate(row_items, 0):
                    if i < len(row_items)-1:
                        outfile.write("%s\n" % item)
                    else:
                        outfile.write("%s" % item)
    return


def get_list_of_parameters(filein, param_column):
    """
    get list of parameters in each subsystem file
    """
    with open(filein, 'r') as infile:
        params = []
        for i, row in enumerate(infile, 0):
            row_split = row.strip().split(',')
            if len(row_split) > 0:
                if row_split[param_column] not in params:
                    params.append(row_split[param_column])
    return params


def get_list_of_variables(filein, parameter, var_column):
    """
    get list of variables for a subsystem[parameter]
    """
    with open(filein, 'r') as infile:
        vars = []
        for i, row in enumerate(infile, 0):
            row_split = row.strip().split(',')
            if parameter in row_split:
                if row_split[var_column] not in vars:
                    vars.append(row_split[var_column])
    return vars


def printFunction(*args):
    if six.PY2:
        print(*args)
        sys.stdout.flush()
    else:
        print(*args, flush=True)


def convert_to_float(s, regex_pat):
    """
    function to convert values to float in a more sensible and somewhat robust way
    """
    match = regex_pat.search(s)
    if match is None:
        if len(s) > 0:
            out = float(s)
        else:
            out = None
    else:
        if len(s) == 0:
            out = None
        else:
            out = s
    return out


def str2float(s, regex_pat):
    """
    function to convert values to float in a more sensible and somewhat robust way
    """
    if s in ["NA", ""]:
        return "NA"
    else:
        match = regex_pat.search(s)
        if match is None:
            out = float(s)
        else:
            out = s
        return out
