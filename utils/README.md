# Utils

## Installing Dependendecies

```sh
pip3 install -r requirements.txt
```

## Example

### Data Stream Annotation

We can quickly annotate a data stream using the `annotate-stream.py` tool.

```sh
curl -s https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.recent.csv | ./annotate-stream.py
```

This adds additional columns indicating if data is valid and, if not, what errors occurred. For example,

```
timestamp,node_id,subsystem,sensor,parameter,value_raw,value_hrf,valid,errors
2019/03/12 18:30:46,001e061130f4,lightsense,hmc5883l,magnetic_field_z,-881,-898.98,1,
2019/03/12 18:30:46,001e061130f4,lightsense,ml8511,intensity,9729,46.273,0,range
2019/03/12 18:30:46,001e061130f4,lightsense,mlx75305,intensity,31398,687.657,0,range
2019/03/12 18:30:46,001e061130f4,lightsense,tmp421,temperature,6352,24.81,1,
2019/03/12 18:30:46,001e061130f4,lightsense,tsl250rd,intensity,9729,23.662,1,
...
```

### Ranking Nodes and Sensors

We can use the data stream annotation to generate a few health reports of the data. These can be used as follows:

```sh
curl -s https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.recent.csv | ./annotate-stream.py | ./rank-nodes.py
```

```sh
curl -s https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.recent.csv | ./annotate-stream.py | ./rank-sensors.py
```

```sh
curl -s https://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/AoT_Chicago.complete.recent.csv | ./annotate-stream.py | ./rank-node-sensors.py
```
