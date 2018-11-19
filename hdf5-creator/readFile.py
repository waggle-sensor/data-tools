#----------+----------+---------------+----------#
#  Script to call the shared library using ctypes
#   Author : Nikhil Garg
#   Email : nikhil.garg@dat61.csiro.au
#----------+----------+---------------+----------#

import os
import sys
import six
import ctypes
from time import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from array_of_things import _readFile, _subsetFile, cast_string, Arguments


def subset_node_subsystem(filein, nodeid):
    """
    interface function for the python wrapper around c function
    """
    file_dir = os.path.dirname(filein)
    file_name = os.path.basename(filein)

    if not os.path.exists(os.path.join(file_dir, "node_names.txt")):
        raise RuntimeError("File node_names.txt doesn't exist in %s" % file_dir)

    if not os.path.exists(os.path.join(file_dir, "subsystem_names.txt")):
        raise RuntimeError("File subsystem_names.txt doesn't exist in %s" % file_dir)

    if not os.path.exists(os.path.join(filein)):
        raise RuntimeError("File %s doesn't exist in %s" % (file_name, file_dir))

    args = Arguments(cast_string("node_names.txt"),
                    cast_string("subsystem_names.txt"),
                    cast_string(file_name),
                    cast_string(nodeid))

    out = _readFile(args)
    if out != 0:
        raise RuntimeError("C function didn't work properly")
    else:
        return out


def subsetFile(filein, fileout, linecount):
    """
    python wrapper for c function to step through a large file and
    write the lines equal and after the line count given

    Arguments:
    ----------
    filein : string, complete path of the file to be read, file should be present
    fileout : string complete path of the file to be written, file should not be present
    linecount : integer,
    """
    if not os.path.exists(filein):
        raise ValueError("File %s doesnt exist" % filein)
    if os.path.exists(fileout):
        raise ValueError("File %s exists, by default it is expected that file should not be present" % fileout)
    out = _subsetFile([cast_string(filein), cast_string(fileout), linecount])
    return out


if __name__ == "__main__":
    start = time()
    args = Arguments(cast_string("node_names.txt"), cast_string("subsystem_names.txt"),
                    cast_string("data.csv"), cast_string("001e06109416"))
    out = readFile(args)
    end = time()
    print(out)
    print(end - start)