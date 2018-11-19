import os
import sys
import six
from time import time
from datetime import datetime, timedelta
import h5py
import numpy as np

try:
    from scipy.interpolate import griddata
except:
    has_scipy=False

try:
    import pandas as pd
except ImportError:
    has_pandas=False

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    import matplotlib.dates as mdates
except ImportError:
    has_pyplot=False

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError:
    has_cartopy=False

try:
    from netCDF4 import date2num, num2date
except ImportError:
    has_ncdf=False


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class h5Data(object):
    """
    Object to read the hdf5 file and parse the children into the attributes of the
    class
    """
    def __init__(self, *args, **kwargs):
        self._filein = None
        if len(args) > 0:
            if isinstance(args[0], str) and os.path.exists(args[0]):
                    self._filein = h5py.File(args[0], mode='r')
        elif len(kwargs) > 0:
            if 'fileIn' in kwargs:
                if isinstance(kwargs['fileIn'], str) and os.path.exists(kwargs['fileIn']):
                    self._filein = h5py.File(kwargs['fileIn'], mode='r')

        self._getattr()
        for item in self._filein:
            if isinstance(self._filein[item], h5py.Group) and item.startswith("node"):
                setattr(self, item, h5node(self._filein[item]))

    def close(self):
        self.__exit__()
        obj_attr = list(self.__dict__.keys())
        for item in obj_attr:
            if isinstance(self.__getattribute__(item), h5node):
                self.__getattribute__(item).close()
            else:
                self.__delattr__(item)

    def _getattr(self):
        if self._filein is not None:
            for item in self._filein.attrs:
                setattr(self, item, self._filein.attrs[item])

    def __exit__(self):
        if self._filein is not None:
            try:
                _ = self._filein.filename
                self._filein.close()
            except ValueError:
                print("File was not open")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}'.format(self.__class__.__name__)


class h5node(object):
    """
    python object to process the node within the hdf5 file
    """
    def __init__(self, *args, **kwargs):
        self.name = "node"
        self._handle = None
        if len(args) > 0:
            if isinstance(args[0], h5py.Group):
                self._handle = args[0]
        elif len(kwargs) > 0:
            if 'node' in kwargs and isinstance(kwargs['node'], h5py.Group):
                self._handle = kwargs['node']

        self._getattr()
        if self._handle is not None:
            self.name = self._handle.name.split('/')[1]
            for item in self._handle:
                if (isinstance(self._handle[item], h5py.Group) and
                    item in ['alphasense', 'metsense', 'chemsense', 'plantower', 'lightsense']):
                    setattr(self, item, h5system(self._handle[item]))

    def close(self):
        obj_attr = list(self.__dict__.keys())
        for item in obj_attr:
            if isinstance(self.__getattribute__(item), h5system):
                self.__getattribute__(item).close()
            else:
                self.__delattr__(item)

    def _getattr(self):
        if self._handle is not None:
            for item in self._handle.attrs:
                setattr(self, item, self._handle.attrs[item])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}.{}'.format(self.__class__.__name__, self.name)


class h5system(object):
    """
    python object for parsing the subsystem from the node
    """
    def __init__(self, *args, **kwargs):
        self.name = "subsystem"
        self._handle = None

        if len(args) > 0:
            if isinstance(args[0], h5py.Group):
                self._handle = args[0]
        elif len(kwargs) > 0:
            if 'subsystem' in kwargs and isinstance(kwargs['subsystem'], h5py.Group):
                self._handle = kwargs['subsystem']

        self._getattr()
        if self._handle is not None:
            self.name = self._handle.name.split('/')[2]
            for item in self._handle:
                if isinstance(self._handle[item], h5py.Group):
                    setattr(self, item, h5sensor(self._handle[item]))

    def close(self):
        obj_attr = list(self.__dict__.keys())
        for item in obj_attr:
            if isinstance(self.__getattribute__(item), h5sensor):
                self.__getattribute__(item).close()
            else:
                self.__delattr__(item)

    def _getattr(self):
        if self._handle is not None:
            for item in self._handle.attrs:
                setattr(self, item, self._handle.attrs[item])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}.{}'.format(self.__class__.__name__, self.name)


class h5sensor(object):
    """python node for the sensor within a subsystem of the node
    """
    def __init__(self, *args, **kwargs):
        self.name = "sensor"
        self._handle = None

        if len(args) > 0:
            if isinstance(args[0], h5py.Group):
                self._handle = args[0]
        elif len(kwargs) > 0:
            if 'sensor' in kwargs and isinstance(kwargs['sensor'], h5py.Group):
                self._handle = kwargs['sensor']

        self._getattr()
        if self._handle is not None:
            self.name = self._handle.name.split('/')[3]
            for item in self._handle:
                if isinstance(self._handle[item], h5py.Dataset):
                    setattr(self, item, h5parameter(self._handle[item]))

    def close(self):
        obj_attr = list(self.__dict__.keys())
        for item in obj_attr:
            if isinstance(self.__getattribute__(item), h5parameter):
                self.__getattribute__(item).close()
            else:
                self.__delattr__(item)

    def _getattr(self):
        if self._handle is not None:
            for item in self._handle.attrs:
                setattr(self, item, self._handle.attrs[item])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}.{}'.format(self.__class__.__name__, self.name)


class h5parameter(object):
    """python object for the variable within the sensor of a node
    """
    def __init__(self, *args, **kwargs):
        self.name = "parameter"
        self.is_sensing = False
        self._handle = None

        if len(args) > 0:
            if isinstance(args[0], h5py.Dataset):
                self._handle = args[0]
        elif len(kwargs) > 0:
            if 'parameter' in kwargs and isinstance(kwargs['parameter'], h5py.Dataset):
                self._handle = kwargs['parameter']

        self._getattr()
        if self._handle is not None:
            self.name = self._handle.name.split('/')[4]
            self._is_sensing()

    def _is_sensing(self):
        if self._handle is not None and isinstance(self._handle, (h5py.Dataset, h5py.Group)):
            if 'kind' in self._handle.attrs and self._handle.attrs['kind'] == "sensing":
                self.is_sensing = True

    def close(self):
        obj_attr = list(self.__dict__.keys())
        for item in obj_attr:
            self.__delattr__(item)

    def _getattr(self):
        if self._handle is not None:
            for item in self._handle.attrs:
                setattr(self, item, self._handle.attrs[item])

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{}.{}'.format(self.__class__.__name__, self.name)


def get_nodes_list(filehandle, subsystem=None, sensor=None, variable=None):
    """
    function to get a list of nodes for varying conditional requirements:

    Cases:
    ======
    1. Get a list of nodes which has a specific subsystem
    2. Get a list of nodes which has a specific sensor under a specific subsystem
    3. Get a list of nodes which has a specific variable from a given sensor on a chosen subsystem

    Arguments:
    ==========
    filehandle : path to hdf5 file or file handle of opened hdf5 file
    subsystem : subsystem within the file (string type), optional
    sensor : sensor within the subsystem of a file (string type), optional
    variable : variable within the sensor under a subsystem of a file (string type), optional

    Returns:
    =======
    node_list : a list of nodes

    Example:
    ========
    >>> #when testing case 1
    >>> get_node_list(h5py_file, subsystem="alphasense")
    >>> #when testing case 2
    >>> get_node_list(h5py_file, subsystem="alphasense", sensor="opc_n2")
    >>> #when testing case 3
    >>> get_node_list(h5py_file, subsystem="alphasense", sensor="opc_n2", variable="pm1")
    """
    if subsystem is not None:
        if not isinstance(subsystem, str):
            raise TypeError("subsystem keyword should be a string")
    if sensor is not None:
        if not isinstance(sensor, str):
            raise TypeError("sensor keyword should be a string")
    if variable is not None:
        if not isinstance(variable, str):
            raise TypeError("variable keyword should be a string")

    if subsystem is not None and sensor is None and variable is not None:
        raise ValueError("When subsystem and variable are provided, sensor cannot be none")
    elif subsystem is None and sensor is None and variable is not None:
        raise ValueError("When variable is provided, subsystem and sensor cannot be none")
    elif subsystem is None and sensor is not None:
        raise ValueError("When sensor is provided, subsystem cannot be none")

    _filehandle = _check_file_handle(filehandle)

    node_list = []
    for node in _filehandle.keys():
        if isinstance(_filehandle[node], h5py.Group):
            if subsystem is not None and sensor is None and variable is None:
                if subsystem in _filehandle[node]:
                    if node not in node_list:
                        node_list.append(node)
            elif subsystem is not None and sensor is not None and variable is None:
                if subsystem in _filehandle[node]:
                    if (isinstance(_filehandle[node][subsystem], h5py.Group) and
                        sensor in _filehandle[node][subsystem]):
                        if node not in node_list:
                            node_list.append(node)
            elif subsystem is not None and sensor is not None and variable is not None:
                if subsystem in _filehandle[node]:
                    if (isinstance(_filehandle[node][subsystem], h5py.Group) and
                        sensor in _filehandle[node][subsystem]):
                            if (isinstance(_filehandle[node][subsystem][sensor], h5py.Group) and
                                variable in _filehandle[node][subsystem][sensor]):
                                if node not in node_list:
                                    node_list.append(node)

    if isinstance(filehandle, str):
        _filehandle.close()

    return node_list


def list_of_subsystem(filehandle, variable=None, node_id=None):
    """
    get a list of subsystem for a specific variable by walking through the hdf5 file

    Arguments:
    ==========
    filehandle : path to hdf5 file or file handle of opened hdf5 file
    variable : variable to be inspected in hdf5 file (string type), optional

    Returns:
    ========
    subsys_list : list of subsystems

    Example:
    ========
    >>> list_of_subsystem("aot_chicago_data.h5", variable="temperature")
    """
    _filehandle = _check_file_handle(filehandle)

    subsys_list = []
    if node_id is not None:
        if isinstance(node_id, str):
            node_list = [node_id]
        elif isinstance(node_id, list):
            node_list = node_id
    else:
        node_list = list(_filehandle.keys())

    for node in node_list:
        if isinstance(_filehandle[node], h5py.Group):
            for subsystem in _filehandle[node]:
                if isinstance(_filehandle[node][subsystem], h5py.Group):
                    for sensor in _filehandle[node][subsystem]:
                        if isinstance(_filehandle[node][subsystem][sensor], h5py.Group):
                            if variable in _filehandle[node][subsystem][sensor]:
                                if (_filehandle[node][subsystem][sensor][variable], h5py.Dataset):
                                    if subsystem not in subsys_list:
                                        subsys_list.append(subsystem)
    if isinstance(filehandle, str):
        _filehandle.close()
    return subsys_list


def list_of_sensors(filehandle, variable=None, node_id=None):
    """
    get a list of sensors for a specific variable by walking through the hdf5 file

    Arguments:
    ==========
    filehandle : path to hdf5 file or file handle of opened hdf5 file
    variable : variable to be inspected in hdf5 file (string type), optional

    Returns:
    ========
    sensor_list : list of sensors

    Example:
    ========
    >>> list_of_sensor("aot_chicago_data.h5", variable="temperature")
    """
    _filehandle = _check_file_handle(filehandle)

    subsys_list = []
    if node_id is not None:
        if isinstance(node_id, str):
            node_list = [node_id]
        elif isinstance(node_id, list):
            node_list = node_id
    else:
        node_list = list(_filehandle.keys())

    sensor_list = []
    for node in node_list:
        if isinstance(_filehandle[node], h5py.Group):
            for subsystem in _filehandle[node]:
                if isinstance(_filehandle[node][subsystem], h5py.Group):
                    for sensor in _filehandle[node][subsystem]:
                        if isinstance(_filehandle[node][subsystem][sensor], h5py.Group):
                            if (variable in _filehandle[node][subsystem][sensor]):
                                if isinstance(_filehandle[node][subsystem][sensor][variable], h5py.Dataset):
                                    if sensor not in sensor_list:
                                        sensor_list.append(sensor)

    if isinstance(filehandle, str):
        _filehandle.close()
    return sensor_list


def get_nodes_location(filehandle, node_list=None):
    """
    get a numpy array of node locations by walking through the hdf5 file

    Arguments:
    =========
    filehandle : either path to hdf5 file or handle of opened hdf5
    node_list : a list of nodes

    Returns:
    ========
    out_location : a numpy record array with longitude, latitude and node id

    Example:
    ========
    >>> get_node_location("aot_chicago_data.h5", node_list=<list_of_nodes>)
    """
    _filehandle = _check_file_handle(filehandle)

    if len(node_list) == 0:
        raise ValueError("Node list cannot be empty")
    elif node_list is None:
        raise ValueError("Node list cannot be none")
    elif not isinstance(node_list, list):
        raise TypeError("node list should be a list")
    count = 0
    idx = []
    for i, node in enumerate(node_list, 0):
        if node in filehandle and isinstance(filehandle[node], h5py.Group):
            count += 1
            idx.append(i)
    if count == 0:
        raise ValueError("No node given in node list found in the file")

    out_location = np.recarray(shape = (count,), formats=["U11", "<f8", "<f8"],
        names=["nodeId", "lon", "lat"])

    for i in idx:
        out_location[i]["lon"] = filehandle[node_list[i]].attrs['lon']
        out_location[i]["lat"] = filehandle[node_list[i]].attrs['lat']
        out_location[i]["nodeId"] = node_list[i]

    if isinstance(filehandle, str):
        _filehandle.close()
    return out_location


def get_date_bounds(filehandle, subsystem, sensor, node_list=None):
    """
    find the minimum and maximum date from the measured data
    to locate the common period
    """
    _filehandle = _check_file_handle(filehandle)

    if node_list is None:
        raise ValueError("node list cannot be none")
    elif len(node_list) == 0:
        raise ValueError("node list cannot be of zero length")
    elif not isinstance(node_list, list):
        raise TypeError("node list should be a list")

    if not isinstance(subsystem, str):
        raise TypeError("subsystem should be of string type")
    if not isinstance(sensor, str):
        raise TypeError("sensor should be of string type")

    count = 0
    idx = []
    for i, node in enumerate(node_list, 0):
        if node in filehandle and isinstance(filehandle[node], h5py.Group):
            count += 1
            idx.append(i)

    if count == 0:
        raise ValueError("No node found in the hdf5 file")
    start_date = np.zeros(shape=(count,), dtype='f4')
    end_date = np.zeros(shape=(count,), dtype='f4')
    for i in range(count):
        if (subsystem in filehandle[node_list[idx[i]]] and
            isinstance(filehandle[node_list[idx[i]]][subsystem], h5py.Group)):
            if (sensor in filehandle[node_list[idx[i]]][subsystem] and
                isinstance(filehandle[node_list[idx[i]]][subsystem][sensor], h5py.Group)):
                if 'time' in filehandle[node_list[idx[i]]][subsystem][sensor]:
                    start_date[i] = filehandle[node_list[idx[i]]][subsystem][sensor]['time'][0]
                    end_date[i] = filehandle[node_list[idx[i]]][subsystem][sensor]['time'][-1]
    return start_date.max(), end_date[end_date > start_date.max()].min()


def get_date_idx_bounds(filehandle, subsystem, sensor, node_list=None):
    """
    find the start and end date index for each node
    """
    _filehandle = _check_file_handle(filehandle)

    if node_list is None:
        raise ValueError("node list cannot be none")
    elif len(node_list) == 0:
        raise ValueError("node list cannot be of zero length")
    elif not isinstance(node_list, list):
        raise TypeError("node list should be a list")

    if not isinstance(subsystem, str):
        raise TypeError("subsystem should be of string type")
    if not isinstance(sensor, str):
        raise TypeError("sensor should be of string type")

    count = 0
    idx = []
    for i, node in enumerate(node_list, 0):
        if node in filehandle and isinstance(filehandle[node], h5py.Group):
            count += 1
            idx.append(i)

    #out_location = np.recarray(shape=(count,), formats=["U11", "<i4", "<i4"],
    #    names=["nodeId", "start", "end"])
    _node = []
    _start = []
    _end = []
    startDate, endDate = get_date_bounds(filehandle, subsystem, sensor,
        node_list=node_list)

    if endDate < startDate:
        raise ValueError("End date cannot be less than start date")

    if startDate == 0 or endDate == 0:
        raise ValueError("Start and end date cannot be zero")
    for i in idx:
        _time = filehandle[node_list[i]][subsystem][sensor]['time']
        time_mask = np.logical_and(_time >= startDate, _time <= endDate)
        if np.any(time_mask):
            _start.append(np.argwhere(time_mask == True).flatten().min())
            _end.append(np.argwhere(time_mask == True).flatten().max())
            _node.append(node_list[i])
    if len(_node) > 0:
        return np.rec.fromarrays([_start, _end, _node,
            [subsystem]*len(_node), [sensor]*len(_node)],
            formats=['<i4', '<i4', 'U11', "U%d" % len(subsystem), "U%d" % len(sensor),],
            names=['start', 'end', 'nodeId', "subsystem", "sensor"])
    else:
        raise ValueError("No node with common period is found")


def get_data_from_file(filehandle, variable, date_limits):
    """
    extract data from the hdf5 file using date_limits information for a
    given variable

    this function works with recursion by exploring the whole path
    """
    out_data = {}
    for item in date_limits:
        idx_s = item['start']
        idx_e = item['end']
        node = item['nodeId']
        subsystem = item["subsystem"]
        sensor = item["sensor"]
        if filehandle.name == "/":
            if node not in out_data:
                out_data[node] = get_data_from_file(filehandle[node], variable,
                    date_limits[date_limits["nodeId"] == node])
        elif filehandle.name == '/%s' % node:
            if subsystem not in out_data:
                out_data[subsystem] = get_data_from_file(filehandle[subsystem],
                    variable, date_limits[date_limits["subsystem"] == subsystem])
        elif filehandle.name == "/%s/%s" % (node, subsystem):
            if sensor not in out_data:
                out_data[sensor] = get_data_from_file(filehandle[sensor],
                    variable, date_limits[date_limits["sensor"] == sensor])
        elif filehandle.name == "/%s/%s/%s" % (node, subsystem, sensor):
            if variable in filehandle:
                # print(node, subsystem, sensor)
                # print(filehandle["time"][idx_s:idx_e].shape, filehandle[variable][idx_s:idx_e].shape)
                return np.c_[filehandle["time"][idx_s:idx_e], filehandle[variable][idx_s:idx_e]]
    return out_data


def item_in_node(filehandle, item_path):
    _filehandle = _check_file_handle(filehandle)
    if isinstance(item_path, str):
        if '/' in item_path and item_path.startswith('/'):
            _path = item_path
        else:
            raise ValueError("Could not understand the item path")
    elif isinstance(item_path, list):
        _path = '/'.join([''] + item_path)
    else:
        raise TypeError("Only a list of path or a path of string type is accepted")

    try:
        dummy = _filehandle[_path]
        flag = True
    except KeyError:
        flag = False

    if isinstance(filehandle, str):
        _filehandle.close()
    return flag


def _check_file_handle(filehandle):
    """
    check whether the filehandle is a string (i.e. path to hdf5) or
    and opened hdf5 file. This function is mostly used internally
    """
    if isinstance(filehandle, h5py.File):
        _filehandle = filehandle
    elif isinstance(filehandle, str):
        if os.path.exists(filehandle):
            _filehandle = h5py.File(filehandle, mode='r')
        else:
            raise ValueError("File %s is not present" % filehandle)
    else:
        raise TypeError("Unable to understand the type of filehandle")
    return _filehandle


if __name__ == "__main__":
    filein = h5py.File("./aot_chicago_data.h5", mode='r')
    variable = "temperature"
    sensor_list = list_of_sensors(filein, variable=variable)
    subsystem_list = list_of_subsystem(filein, variable=variable)

    _sensor = sensor_list[1]
    _subsystem = subsystem_list[0]

    node_list = get_nodes_list(filein, subsystem=_subsystem, sensor=_sensor,
        variable=variable)
    node_locs = get_nodes_location(filein, node_list)
    time_units = filein[node_list[0]][_subsystem][_sensor]['time'].attrs['units']
    startDate, endDate = get_date_bounds(filein, subsystem_list[0], sensor_list[0],
        node_list=node_list)
    date_idx_limits = get_date_idx_bounds(filein, _subsystem, _sensor,
        node_list=node_list)
    # subsystem_list = list_of_subsystem(filein, variable=variable, node_id=node_list[0])
    # sensor_list = list_of_sensors(filein, variable=variable, node_id=node_list[0])

    # count = 0
    # for _subsys in subsystem_list:
    #     for _sense in sensor_list:
    #         if item_in_node(filein, [node_list[0],_subsys,_sense]):
    #             _date_limits = get_date_idx_bounds(filein, _subsys, _sense,
    #                 node_list=[node_list[0]])
    #             if count == 0:
    #                 date_idx_limits = _date_limits.tolist()
    #             else:
    #                 date_idx_limits += _date_limits.tolist()
    #             count += 1
    # date_idx_limits = np.rec.fromrecords(date_idx_limits,
    #     names=['start', 'end', 'nodeId', 'subsystem', 'sensor'])
    data_temperature = get_data_from_file(filein, "temperature",
        date_idx_limits)
    node_locs = get_nodes_location(filein, list(data_temperature.keys()))

    # fig = plt.figure(1)
    # ax = fig.add_subplot(111)
    # ax.plot(data_temperature['node_109416']['metsense']['bmp180'][0],
    #     data_temperature['node_109416']['metsense']['bmp180'][1])
    # plt.show()

    xll = node_locs['lon'].min()
    xur = node_locs['lon'].max()
    yll = node_locs['lat'].min()
    yur = node_locs['lat'].max()

    land_50m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                            edgecolor='face',
                                            facecolor=cfeature.COLORS['land'])

    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    ax.add_feature(land_50m)
    ax.coastlines('10m')
    ax.set_extent([xll - 0.1, xur + 0.1, yll - 0.1, yur + 0.1])

    for i in range(len(node_locs)):
        ax.plot(node_locs[i]['lon'], node_locs[i]['lat'], marker='s', markersize=4,
            mfc='k', mec='k', linestyle='')

    grid_lon = np.linspace(xll, xur, 100)
    grid_lat = np.linspace(yll, yur, 100)

    Lon, Lat = np.meshgrid(grid_lon, grid_lat)

    point_temp = []
    for node in data_temperature:
        point_temp.append(data_temperature[node]['chemsense']['at1'][0, 1])

    temp2d = griddata(np.c_[node_locs['lon'], node_locs['lat']],
        point_temp, np.c_[Lon.ravel(), Lat.ravel()])
    temp2d = temp2d.reshape(Lon.shape)

    fig = plt.figure(2)
    ax = fig.add_subplot(111)
    for item in data_temperature:
        ax.plot(data_temperature[item]['chemsense']['at1'][:, 0],
            data_temperature[item]['chemsense']['at1'][:, 1])

    fig = plt.figure(3)
    ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
    cs = ax.contourf(Lon, Lat, temp2d, levels=np.linspace(10, 20, 21), cmap=plt.cm.plasma)
    fig.colorbar(cs, ax=ax, shrink=0.8, fraction=0.1)
    plt.show()

    filein.close()