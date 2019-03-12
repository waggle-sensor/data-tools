#!/usr/bin/env python3
import argparse
import csv
import sys

inf = float('inf')

valid_hrf_range = {
    ('chemsense', 'co', 'concentration'): (0, 1000),
    ('chemsense', 'h2s', 'concentration'): (0, 50),
    ('chemsense', 'no2', 'concentration'): (0, 20),
    ('chemsense', 'o3', 'concentration'): (0, 20),
    ('chemsense', 'oxidizing_gases', 'concentration'): (0, 100),
    ('chemsense', 'reducing_gases', 'concentration'): (0, 20),
    ('chemsense', 'so2', 'concentration'): (0, 20),
    ('alphasense', 'opc_n2', 'bins'): (0, inf),
    ('plantower', 'pms7003', '10um_particle'): (0, inf),
    ('plantower', 'pms7003', '1um_particle'): (0, inf),
    ('plantower', 'pms7003', '2_5um_particle'): (0, inf),
    ('plantower', 'pms7003', '5um_particle'): (0, inf),
    ('plantower', 'pms7003', 'point_3um_particle'): (0, inf),
    ('plantower', 'pms7003', 'point_5um_particle'): (0, inf),
    ('alphasense', 'opc_n2', 'pm1'): (0, inf),
    ('plantower', 'pms7003', 'pm1_atm'): (0, inf),
    ('alphasense', 'opc_n2', 'pm10'): (0, inf),
    ('plantower', 'pms7003', 'pm10_atm'): (0, inf),
    ('alphasense', 'opc_n2', 'pm2_5'): (0, inf),
    ('plantower', 'pms7003', 'pm25_atm'): (0, inf),
    ('metsense', 'hih4030', 'humidity'): (0, 100),
    ('metsense', 'htu21d', 'humidity'): (0, 100),
    ('metsense', 'bmp180', 'pressure'): (300, 1100),
    ('metsense', 'bmp180', 'temperature'): (-40, 85),
    ('metsense', 'htu21d', 'temperature'): (-40, 125),
    ('metsense', 'pr103j2', 'temperature'): (-55, 80),
    ('metsense', 'tmp112', 'temperature'): (-40, 125),
    ('metsense', 'tsys01', 'temperature'): (-40, 125),
    ('audio', 'microphone', 'octave_1_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_10_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_2_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_3_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_4_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_5_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_6_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_7_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_8_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_9_intensity'): (-inf, 140),
    ('audio', 'microphone', 'octave_total_intensity'): (-inf, 140),
    ('lightsense', 'tsl260rd', 'intensity'): (0, 132),
    ('lightsense', 'apds_9006_020', 'intensity'): (0, 1000),
    ('lightsense', 'mlx75305', 'intensity'): (0, 160),
    ('lightsense', 'tsl250rd', 'intensity'): (0, 124),
    ('lightsense', 'hmc5883l', 'magnetic_field_x'): (-8000, 8000),
    ('lightsense', 'hmc5883l', 'magnetic_field_y'): (-8000, 8000),
    ('lightsense', 'hmc5883l', 'magnetic_field_z'): (-8000, 8000),
    ('metsense', 'spv1840lr5h_b', 'intensity'): (0, 121),
    ('lightsense', 'ml8511', 'intensity'): (0, 15),
    ('metsense', 'mma8452q', 'acceleration_x'): (-8000, 8000),
    ('metsense', 'mma8452q', 'acceleration_y'): (-8000, 8000),
    ('metsense', 'mma8452q', 'acceleration_z'): (-8000, 8000),
    ('ep', 'loadavg', 'load_1'): (0, inf),
    ('ep', 'loadavg', 'load_10'): (0, inf),
    ('ep', 'loadavg', 'load_5'): (0, inf),
    ('ep', 'mem', 'free'): (0, inf),
    ('ep', 'mem', 'total'): (0, inf),
    ('ep', 'uptime', 'idletime'): (0, inf),
    ('ep', 'uptime', 'uptime'): (0, inf),
    ('lightsense', 'hih6130', 'humidity'): (0, 100),
    ('chemsense', 'si1145', 'ir_intensity'): (0, inf),
    ('chemsense', 'si1145', 'visible_light_intensity'): (0, inf),
    ('lightsense', 'hih6130', 'temperature'): (-25, 85),
    ('wagman', 'htu21d', 'humidity'): (0, 100),
    ('wagman', 'htu21d', 'temperature'): (-40, 125),
    ('wagman', 'temperatures', 'battery'): (-55, 125),
    ('wagman', 'temperatures', 'brainplate'): (-55, 125),
    ('wagman', 'temperatures', 'ep_heatsink'): (-55, 125),
    ('wagman', 'temperatures', 'nc_heatsink'): (-55, 125),
    ('wagman', 'temperatures', 'powersupply'): (-55, 125),
    ('lightsense', 'tmp421', 'temperature'): (-55, 127),
    ('chemsense', 'si1145', 'uv_intensity'): (-inf, inf),
    ('nc', 'loadavg', 'load_1'): (0, inf),
    ('nc', 'loadavg', 'load_10'): (0, inf),
    ('nc', 'loadavg', 'load_5'): (0, inf),
    ('nc', 'mem', 'free'): (0, inf),
    ('nc', 'mem', 'total'): (0, inf),
    ('nc', 'net_broadband', 'rx'): (0, inf),
    ('nc', 'net_broadband', 'tx'): (0, inf),
    ('nc', 'net_lan', 'rx'): (0, inf),
    ('nc', 'net_lan', 'tx'): (0, inf),
    ('nc', 'net_usb', 'rx'): (0, inf),
    ('nc', 'net_usb', 'tx'): (0, inf),
    ('nc', 'uptime', 'idletime'): (0, inf),
    ('nc', 'uptime', 'uptime'): (0, inf),
    ('alphasense', 'opc_n2', 'sample_flow_rate'): (-inf, inf),
    ('chemsense', 'lps25h', 'pressure'): (260, 1260),
    ('chemsense', 'sht25', 'humidity'): (0, 100),
    ('chemsense', 'chemsense', 'id'): (-inf, inf),
    ('metsense', 'metsense', 'id'): (-inf, inf),
    ('alphasense', 'opc_n2', 'fw'): (-inf, inf),
    ('metsense', 'tsl250rd', 'intensity'): (0, 124),
    ('chemsense', 'lps25h', 'temperature'): (-30, 105),
    ('alphasense', 'opc_n2', 'sampling_period'): (-inf, inf),
    ('chemsense', 'at0', 'temperature'): (-40, 125),
    ('chemsense', 'at1', 'temperature'): (-40, 125),
    ('chemsense', 'at2', 'temperature'): (-40, 125),
    ('chemsense', 'at3', 'temperature'): (-40, 125),
    ('chemsense', 'sht25', 'temperature'): (-40, 125),
    ('wagman', 'current', 'cs'): (0, 8000),
    ('wagman', 'current', 'ep'): (0, 8000),
    ('wagman', 'current', 'nc'): (0, 8000),
    ('wagman', 'current', 'wagman'): (0, 8000),
    ('wagman', 'failures', 'cs'): (0, inf),
    ('wagman', 'failures', 'ep'): (0, inf),
    ('wagman', 'failures', 'nc'): (0, inf),
    ('wagman', 'heartbeat', 'cs'): (0, inf),
    ('wagman', 'heartbeat', 'ep'): (0, inf),
    ('wagman', 'heartbeat', 'nc'): (0, inf),
    ('wagman', 'enabled', 'cs'): (0, 1),
    ('wagman', 'enabled', 'ep'): (0, 1),
    ('wagman', 'enabled', 'nc'): (0, 1),
    ('wagman', 'uptime', 'uptime'): (0, inf),
}


def between(x, r):
    return r[0] <= x and x <= r[1]


def validator(x, s):
    return between(x, valid_hrf_range[s])


reader = csv.DictReader(sys.stdin)
writer = csv.writer(sys.stdout)

writer.writerow([
    'timestamp',
    'node_id',
    'subsystem',
    'sensor',
    'parameter',
    'value_raw',
    'value_hrf',
    'valid',
    'errors',
])

parser = argparse.ArgumentParser()
parser.add_argument('--env', action='store_true')
args = parser.parse_args()

for row in reader:
    if args.env and row['subsystem'] not in ['metsense', 'lightsense', 'chemsense']:
        continue

    series = (row['subsystem'], row['sensor'], row['parameter'])
    errors = []

    try:
        value_hrf = float(row['value_hrf'])
    except ValueError:
        continue
    
    try:
        valid = validator(value_hrf, series)
    except KeyError:
        errors.append('noent')

    if not valid:
        errors.append('range')

    writer.writerow([
        row['timestamp'],
        row['node_id'],
        row['subsystem'],
        row['sensor'],
        row['parameter'],
        row['value_raw'],
        row['value_hrf'],
        int(valid),
        ' '.join(errors),
    ])
