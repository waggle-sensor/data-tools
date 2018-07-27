# Moving Averages Command Line Tool

## Requirements
This tool requires Python3.

## Step-by-Step Instructions for Creating Moving Averages
1. Download and unpackage a complete node dataset. Make sure to complete the step that unpackages the data.csv.gz archive.
4. Run the movingAvg.py tool from the command line: 
```python3 movingAvg.py -i /PATH_TO_COMPLETE_NODE_DATA_SET -t #x```

Replace ```/PATH_TO_COMPLETE_NODE_DATA_SET``` with the path to the unpackaged compete node data set from step 1, ```#``` with an integer and ```x``` with one of the following characters: ```'s','m','h', or 'd'```. Remember, the directory path specified must contain the following five files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv.

## Examples

### Moving Average Over a 30 Min. Period

```
@ermac:~/data-tools/moving-average-tool$ python3 movingAvg.py -i ../AoT_Portland.complete.2018-07-03 -t 30m
...
2018/01/26 19:56:42,001e0610e545,chemsense,sht25,temperature,2139.0299999999997,72,29.708749999999995
2018/01/26 19:56:42,001e0610e545,chemsense,si1145,ir_intensity,NA,0,NA
2018/01/26 19:56:42,001e0610e545,chemsense,si1145,uv_intensity,NA,0,NA
2018/01/26 19:56:42,001e0610e545,chemsense,si1145,visible_light_intensity,NA,0,NA
2018/01/26 19:56:42,001e0610e545,chemsense,so2,concentration,NA,0,NA
2018/01/26 19:56:42,001e0610e545,lightsense,apds_9006_020,intensity,51.49899999999997,72,0.7152638888888885
2018/01/26 19:56:42,001e0610e545,lightsense,hih6130,humidity,1506.240000000001,72,20.920000000000012
2018/01/26 19:56:42,001e0610e545,lightsense,hih6130,temperature,2206.080000000002,72,30.64000000000003
2018/01/26 19:56:42,001e0610e545,lightsense,hmc5883l,magnetic_field_x,-6665.450999999998,72,-92.57570833333331
2018/01/26 19:56:42,001e0610e545,lightsense,hmc5883l,magnetic_field_y,35805.45900000001,72,497.2980416666668
2018/01/26 19:56:42,001e0610e545,lightsense,hmc5883l,magnetic_field_z,44094.89700000002,72,612.4291250000002
2018/01/26 19:56:42,001e0610e545,lightsense,ml8511,intensity,2822.7109999999993,72,39.20431944444444
2018/01/26 19:56:42,001e0610e545,lightsense,mlx75305,intensity,2340.036,72,32.5005
2018/01/26 19:56:42,001e0610e545,lightsense,tmp421,temperature,3042.9299999999994,72,42.262916666666655
2018/01/26 19:56:42,001e0610e545,lightsense,tsl250rd,intensity,123.54999999999998,72,1.715972222222222
2018/01/26 19:56:42,001e0610e545,lightsense,tsl260rd,intensity,1809.0919999999994,72,25.12627777777777
2018/01/26 19:56:42,001e0610e545,metsense,bmp180,pressure,75253.31999999999,72,1045.185
2018/01/26 19:56:42,001e0610e545,metsense,bmp180,temperature,4599.900000000001,72,63.88750000000001
2018/01/26 19:56:42,001e0610e545,metsense,hih4030,humidity,3026.919999999998,72,42.04055555555553
2018/01/26 19:56:42,001e0610e545,metsense,htu21d,humidity,694.02,72,9.639166666666666
2018/01/26 19:56:42,001e0610e545,metsense,htu21d,temperature,2095.55,72,29.104861111111113
2018/01/26 19:56:42,001e0610e545,metsense,metsense,id,0179c3e21700,0,0179c3e21700
2018/01/26 19:56:42,001e0610e545,metsense,mma8452q,acceleration_x,-1242.1959999999997,72,-17.252722222222218
2018/01/26 19:56:42,001e0610e545,metsense,mma8452q,acceleration_y,-130.858,72,-1.8174722222222224
2018/01/26 19:56:42,001e0610e545,metsense,mma8452q,acceleration_z,-72589.845,72,-1008.1922916666667
2018/01/26 19:56:42,001e0610e545,metsense,pr103j2,temperature,2222.2999999999984,72,30.865277777777756
2018/01/26 19:56:42,001e0610e545,metsense,spv1840lr5h_b,intensity,4023.639999999997,72,55.88388888888885
2018/01/26 19:56:42,001e0610e545,metsense,tmp112,temperature,2119.3699999999994,72,29.435694444444437
2018/01/26 19:56:42,001e0610e545,metsense,tsl250rd,intensity,585.2670000000003,72,8.128708333333337
2018/01/26 19:56:42,001e0610e545,metsense,tsys01,temperature,2166.0599999999995,72,30.08416666666666
...
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,bins,"13,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0",0,"13,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0"
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,fw,1310.4000000000017,72,18.200000000000024
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,id,OPC-N2 176180612    ,0,OPC-N2 176180612    
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,pm1,6.497,72,0.09023611111111111
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,pm10,7.481999999999998,72,0.10391666666666664
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,pm2_5,7.445999999999998,72,0.10341666666666664
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,sample_flow_rate,192.63918999999999,72,2.6755443055555554
2018/01/27 03:01:24,001e0610e545,alphasense,opc_n2,sampling_period,1805.20689,72,25.072317916666666
2018/01/27 03:01:24,001e0610e545,chemsense,at0,temperature,2174.6200000000003,72,30.20305555555556
2018/01/27 03:01:24,001e0610e545,chemsense,at1,temperature,2211.890000000001,72,30.720694444444455
2018/01/27 03:01:24,001e0610e545,chemsense,at2,temperature,2263.5399999999995,72,31.43805555555555
2018/01/27 03:01:24,001e0610e545,chemsense,at3,temperature,2313.7500000000023,72,32.1354166666667
2018/01/27 03:01:24,001e0610e545,chemsense,chemsense,id,5410ec38a483,0,5410ec38a483
2018/01/27 03:01:24,001e0610e545,chemsense,co,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,h2s,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,lps25h,pressure,70466.39999999998,71,992.4845070422532
2018/01/27 03:01:24,001e0610e545,chemsense,lps25h,temperature,2515.7799999999993,71,35.43352112676055
2018/01/27 03:01:24,001e0610e545,chemsense,no2,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,o3,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,oxidizing_gases,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,reducing_gases,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,sht25,humidity,980.6099999999993,71,13.811408450704215
2018/01/27 03:01:24,001e0610e545,chemsense,sht25,temperature,2208.420000000001,71,31.104507042253534
2018/01/27 03:01:24,001e0610e545,chemsense,si1145,ir_intensity,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,si1145,uv_intensity,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,si1145,visible_light_intensity,NA,0,NA
2018/01/27 03:01:24,001e0610e545,chemsense,so2,concentration,NA,0,NA
2018/01/27 03:01:24,001e0610e545,lightsense,apds_9006_020,intensity,58.20700000000004,72,0.8084305555555562
2018/01/27 03:01:24,001e0610e545,lightsense,hih6130,humidity,1506.240000000001,72,20.920000000000012
2018/01/27 03:01:24,001e0610e545,lightsense,hih6130,temperature,2206.080000000002,72,30.64000000000003
2018/01/27 03:01:24,001e0610e545,lightsense,hmc5883l,magnetic_field_x,-5521.825999999998,72,-76.69202777777775
2018/01/27 03:01:24,001e0610e545,lightsense,hmc5883l,magnetic_field_y,35050.91200000001,72,486.8182222222224
2018/01/27 03:01:24,001e0610e545,lightsense,hmc5883l,magnetic_field_z,42098.98400000001,72,584.7081111111113
2018/01/27 03:01:24,001e0610e545,lightsense,ml8511,intensity,2722.061999999998,72,37.80641666666664
2018/01/27 03:01:24,001e0610e545,lightsense,mlx75305,intensity,-118.741,72,-1.6491805555555556
2018/01/27 03:01:24,001e0610e545,lightsense,tmp421,temperature,3515.8000000000015,72,48.83055555555558
2018/01/27 03:01:24,001e0610e545,lightsense,tsl250rd,intensity,-1.9439999999999977,72,-0.02699999999999997
2018/01/27 03:01:24,001e0610e545,lightsense,tsl260rd,intensity,1795.2029999999988,72,24.933374999999984
2018/01/27 03:01:24,001e0610e545,metsense,bmp180,pressure,75120.51999999999,72,1043.3405555555555
2018/01/27 03:01:24,001e0610e545,metsense,bmp180,temperature,4724.799999999996,72,65.62222222222216
2018/01/27 03:01:24,001e0610e545,metsense,hih4030,humidity,2774.37,72,38.532916666666665
2018/01/27 03:01:24,001e0610e545,metsense,htu21d,humidity,387.8199999999999,72,5.386388888888887
2018/01/27 03:01:24,001e0610e545,metsense,htu21d,temperature,2238.5299999999993,72,31.090694444444434
2018/01/27 03:01:24,001e0610e545,metsense,metsense,id,0179c3e21700,0,0179c3e21700
2018/01/27 03:01:24,001e0610e545,metsense,mma8452q,acceleration_x,-1233.4039999999998,72,-17.130611111111108
2018/01/27 03:01:24,001e0610e545,metsense,mma8452q,acceleration_y,-187.49900000000014,72,-2.6041527777777795
2018/01/27 03:01:24,001e0610e545,metsense,mma8452q,acceleration_z,-72192.38299999999,72,-1002.671986111111
2018/01/27 03:01:24,001e0610e545,metsense,pr103j2,temperature,2348.9999999999977,72,32.62499999999997
2018/01/27 03:01:24,001e0610e545,metsense,spv1840lr5h_b,intensity,4064.919999999994,72,56.45722222222214
2018/01/27 03:01:24,001e0610e545,metsense,tmp112,temperature,2249.89,72,31.24847222222222
2018/01/27 03:01:24,001e0610e545,metsense,tsl250rd,intensity,0.0,72,0.0
2018/01/27 03:01:24,001e0610e545,metsense,tsys01,temperature,2292.390000000001,72,31.83875000000001
...
```

### Moving Average Over a 1 Hr. Period
```
@ermac:~/data-tools/moving-average-tool$ python3 movingAvg.py -i ../AoT_Portland.complete.2018-07-03 -t 1h
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,bins,"57,20,13,4,0,1,0,0,0,0,0,0,0,0,0,0",0,"57,20,13,4,0,1,0,0,0,0,0,0,0,0,0,0"
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,fw,2620.799999999998,144,18.199999999999985
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,id,OPC-N2 176180608    ,0,OPC-N2 176180608    
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,pm1,95.77399999999999,144,0.6650972222222221
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,pm10,133.09699999999995,144,0.9242847222222219
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,pm2_5,123.59,144,0.8582638888888889
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,sample_flow_rate,434.0777500000001,144,3.0144288194444453
2018/01/26 20:39:21,001e06113a07,alphasense,opc_n2,sampling_period,3605.8902899999994,144,25.040904791666662
2018/01/26 20:39:21,001e06113a07,chemsense,at0,temperature,4382.489999999997,144,30.43395833333331
2018/01/26 20:39:21,001e06113a07,chemsense,at1,temperature,4482.620000000001,144,31.12930555555556
2018/01/26 20:39:21,001e06113a07,chemsense,at2,temperature,4660.79,144,32.366597222222225
2018/01/26 20:39:21,001e06113a07,chemsense,at3,temperature,4808.789999999998,144,33.39437499999999
2018/01/26 20:39:21,001e06113a07,chemsense,chemsense,id,5410ec38a76e,0,5410ec38a76e
2018/01/26 20:39:21,001e06113a07,chemsense,co,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,h2s,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,lps25h,pressure,143421.55999999997,144,995.9830555555553
2018/01/26 20:39:21,001e06113a07,chemsense,lps25h,temperature,4928.219999999997,144,34.223749999999974
2018/01/26 20:39:21,001e06113a07,chemsense,no2,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,o3,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,oxidizing_gases,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,reducing_gases,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,sht25,humidity,3214.569999999992,144,22.323402777777723
2018/01/26 20:39:21,001e06113a07,chemsense,sht25,temperature,4515.210000000003,143,31.574895104895123
2018/01/26 20:39:21,001e06113a07,chemsense,si1145,ir_intensity,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,si1145,uv_intensity,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,si1145,visible_light_intensity,NA,0,NA
2018/01/26 20:39:21,001e06113a07,chemsense,so2,concentration,NA,0,NA
2018/01/26 20:39:21,001e06113a07,lightsense,apds_9006_020,intensity,121.93600000000006,144,0.8467777777777782
2018/01/26 20:39:21,001e06113a07,lightsense,hih6130,humidity,3113.2799999999897,144,21.61999999999993
2018/01/26 20:39:21,001e06113a07,lightsense,hih6130,temperature,4904.640000000004,144,34.06000000000003
2018/01/26 20:39:21,001e06113a07,lightsense,hmc5883l,magnetic_field_x,-9055.449999999999,144,-62.88506944444444
2018/01/26 20:39:21,001e06113a07,lightsense,hmc5883l,magnetic_field_y,73217.26399999998,144,508.4532222222221
2018/01/26 20:39:21,001e06113a07,lightsense,hmc5883l,magnetic_field_z,91143.87500000015,144,632.9435763888899
2018/01/26 20:39:21,001e06113a07,lightsense,ml8511,intensity,5746.142000000003,144,39.9037638888889
2018/01/26 20:39:21,001e06113a07,lightsense,mlx75305,intensity,3900.492000000006,144,27.08675000000004
2018/01/26 20:39:21,001e06113a07,lightsense,tmp421,temperature,7050.479999999997,144,48.961666666666645
2018/01/26 20:39:21,001e06113a07,lightsense,tsl250rd,intensity,3292.700000000004,144,22.86597222222225
2018/01/26 20:39:21,001e06113a07,lightsense,tsl260rd,intensity,5281.472999999999,144,36.676895833333326
2018/01/26 20:39:21,001e06113a07,metsense,bmp180,pressure,134891.22000000003,144,936.7445833333336
2018/01/26 20:39:21,001e06113a07,metsense,bmp180,temperature,8230.699999999992,144,57.15763888888883
2018/01/26 20:39:21,001e06113a07,metsense,hih4030,humidity,5971.189999999999,144,41.46659722222221
2018/01/26 20:39:21,001e06113a07,metsense,htu21d,humidity,1430.5799999999995,144,9.934583333333329
2018/01/26 20:39:21,001e06113a07,metsense,htu21d,temperature,4334.110000000001,144,30.097986111111116
2018/01/26 20:39:21,001e06113a07,metsense,metsense,id,01d0e0e21700,0,01d0e0e21700
2018/01/26 20:39:21,001e06113a07,metsense,mma8452q,acceleration_x,-2578.1289999999985,144,-17.903673611111103
2018/01/26 20:39:21,001e06113a07,metsense,mma8452q,acceleration_y,2634.777000000002,144,18.297062500000013
2018/01/26 20:39:21,001e06113a07,metsense,mma8452q,acceleration_z,-142208.98400000008,144,-987.5623888888895
2018/01/26 20:39:21,001e06113a07,metsense,pr103j2,temperature,4608.999999999988,144,32.006944444444365
2018/01/26 20:39:21,001e06113a07,metsense,spv1840lr5h_b,intensity,8100.600000000007,144,56.25416666666671
2018/01/26 20:39:21,001e06113a07,metsense,tmp112,temperature,4443.669999999998,144,30.858819444444432
2018/01/26 20:39:21,001e06113a07,metsense,tsl250rd,intensity,1193.643,144,8.2891875
2018/01/26 20:39:21,001e06113a07,metsense,tsys01,temperature,4524.310000000001,144,31.418819444444452
...
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,bins,"28,10,0,0,1,1,0,0,0,0,0,0,0,0,0,0",0,"28,10,0,0,1,1,0,0,0,0,0,0,0,0,0,0"
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,fw,2620.799999999998,144,18.199999999999985
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,id,OPC-N2 176180608    ,0,OPC-N2 176180608    
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,pm1,44.636,144,0.30997222222222226
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,pm10,57.67799999999996,144,0.4005416666666664
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,pm2_5,56.101000000000006,144,0.3895902777777778
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,sample_flow_rate,429.18768999999975,144,2.9804700694444426
2018/01/27 00:01:25,001e06113a07,alphasense,opc_n2,sampling_period,3603.5753999999974,144,25.02482916666665
2018/01/27 00:01:25,001e06113a07,chemsense,at0,temperature,4320.260000000001,144,30.001805555555563
2018/01/27 00:01:25,001e06113a07,chemsense,at1,temperature,4406.730000000001,144,30.602291666666677
2018/01/27 00:01:25,001e06113a07,chemsense,at2,temperature,4569.470000000004,144,31.73243055555558
2018/01/27 00:01:25,001e06113a07,chemsense,at3,temperature,4707.359999999999,144,32.68999999999999
2018/01/27 00:01:25,001e06113a07,chemsense,chemsense,id,5410ec38a76e,0,5410ec38a76e
2018/01/27 00:01:25,001e06113a07,chemsense,co,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,h2s,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,lps25h,pressure,143336.17,144,995.3900694444445
2018/01/27 00:01:25,001e06113a07,chemsense,lps25h,temperature,4840.740000000001,144,33.61625000000001
2018/01/27 00:01:25,001e06113a07,chemsense,no2,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,o3,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,oxidizing_gases,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,reducing_gases,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,sht25,humidity,3075.899999999999,144,21.360416666666662
2018/01/27 00:01:25,001e06113a07,chemsense,sht25,temperature,4462.879999999998,144,30.99222222222221
2018/01/27 00:01:25,001e06113a07,chemsense,si1145,ir_intensity,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,si1145,uv_intensity,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,si1145,visible_light_intensity,NA,0,NA
2018/01/27 00:01:25,001e06113a07,chemsense,so2,concentration,NA,0,NA
2018/01/27 00:01:25,001e06113a07,lightsense,apds_9006_020,intensity,127.06200000000007,144,0.8823750000000005
2018/01/27 00:01:25,001e06113a07,lightsense,hih6130,humidity,3113.2799999999897,144,21.61999999999993
2018/01/27 00:01:25,001e06113a07,lightsense,hih6130,temperature,4904.640000000004,144,34.06000000000003
2018/01/27 00:01:25,001e06113a07,lightsense,hmc5883l,magnetic_field_x,-9137.254000000003,144,-63.453152777777795
2018/01/27 00:01:25,001e06113a07,lightsense,hmc5883l,magnetic_field_y,72092.726,144,500.6439305555555
2018/01/27 00:01:25,001e06113a07,lightsense,hmc5883l,magnetic_field_z,90616.32300000003,144,629.2800208333335
2018/01/27 00:01:25,001e06113a07,lightsense,ml8511,intensity,5722.318000000008,144,39.7383194444445
2018/01/27 00:01:25,001e06113a07,lightsense,mlx75305,intensity,52.564,144,0.3650277777777778
2018/01/27 00:01:25,001e06113a07,lightsense,tmp421,temperature,7182.840000000003,144,49.88083333333336
2018/01/27 00:01:25,001e06113a07,lightsense,tsl250rd,intensity,3289.6470000000018,144,22.844770833333346
2018/01/27 00:01:25,001e06113a07,lightsense,tsl260rd,intensity,-3.0359999999999934,144,-0.021083333333333287
2018/01/27 00:01:25,001e06113a07,metsense,bmp180,pressure,134835.56999999998,144,936.3581249999999
2018/01/27 00:01:25,001e06113a07,metsense,bmp180,temperature,8152.399999999998,144,56.61388888888887
2018/01/27 00:01:25,001e06113a07,metsense,hih4030,humidity,5849.63,144,40.62243055555555
2018/01/27 00:01:25,001e06113a07,metsense,htu21d,humidity,1269.2400000000002,144,8.814166666666669
2018/01/27 00:01:25,001e06113a07,metsense,htu21d,temperature,4285.61,144,29.761180555555555
2018/01/27 00:01:25,001e06113a07,metsense,metsense,id,01d0e0e21700,0,01d0e0e21700
2018/01/27 00:01:25,001e06113a07,metsense,mma8452q,acceleration_x,-2576.1789999999996,144,-17.89013194444444
2018/01/27 00:01:25,001e06113a07,metsense,mma8452q,acceleration_y,2542.968000000002,144,17.659500000000016
2018/01/27 00:01:25,001e06113a07,metsense,mma8452q,acceleration_z,-142483.39300000004,144,-989.4680069444447
2018/01/27 00:01:25,001e06113a07,metsense,pr103j2,temperature,4473.100000000002,144,31.06319444444446
2018/01/27 00:01:25,001e06113a07,metsense,spv1840lr5h_b,intensity,8190.040000000012,144,56.87527777777786
2018/01/27 00:01:25,001e06113a07,metsense,tmp112,temperature,4367.82,144,30.33208333333333
2018/01/27 00:01:25,001e06113a07,metsense,tsl250rd,intensity,0.0,144,0.0
2018/01/27 00:01:25,001e06113a07,metsense,tsys01,temperature,4424.560000000001,144,30.72611111111112
```

## Detailed Description
This tool will calculate a simple moving average (an arithmetic moving average calculated by adding recent data points to the averaging window and then dividing that by the number of time periods in the calculation average) from a complete node data set by averaging sensor values for time ranged windows specified by the user.

### Input
The command line tool `movingAvg.py` takes in a directory path and a time period. The directory path must be the full path to an unpackaged complete node data set (data sets located here: https://github.com/waggle-sensor/waggle/tree/master/data). This path must must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv. The tool will confirm that the aformentioned files exist in the passed in directory before allowing the user to begin reducing data. The time period specified determines the time range window for calculating a simple moving average (e.g. over a span of 5 mins., 1 hr., 1 day, etc.). This time ranged window will move through the data in the data.csv file. For each sensor on each node, the tool will append new sensor values to the time ranged window and throw away values outside of the time ranged window. It will constantly calculate the average of the values in this window, which becomes the simple moving average as it parses through the data. 

### Output
This tool will read the data.csv file located in the passed in directory path, parse through the large data.csv data set, and create moving averages for pieces of data (sensor values) over the time range window period given by the user. It will then create a new movingAvgData.csv file. The final output of the movingAvg.py tool will be a directory that contains the moving average data set (movingAvgData.csv) and the extra metadata files (nodes.csv, provenance.csv, README.md, and sensors.csv) from the passed in unpackaged complete node data set directory path.

**Important:** This tool has not been optimized yet and is time-window dependant; thus it will take a **very** long time (read: several days) to create moving averages for large data sets (> a few Gb) or for larger averaging time period windows (> 12h). It is **highly** recommended that a reduced data set, or an excerpt from the data.csv file, is used with this tool.

## How to Use movingAvg.py
When typing on the terminal, the tool takes in two parameters with identifiers: input directory path (```-i, --input```) and averaging window period (```-t, --time```). 

**Input:** The path to the unpackaged complete node data set (must contain the files: data.csv, nodes.csv, provenance.csv, README.md, and sensors.csv).

**Period:** The averaging window period. This parameter should be in the format ```-t #x ``` where ```#``` is an integer and ```x``` is one of the following characters: ```'s','m','h', or 'd'```. The characters represent seconds, minutes, hours, and days, respectively.

**Note:** User is not allowed to enter anything less than 24 seconds because it is how often data is received and an average could not be calculated for anything lower.
**Note:** The movingAvgData.csv output file will have the headers: ```timestamp,node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_moving_average```.

Terminal command format should be like this example: 

```python3 movingAvg.py -i /home/waggle-student/Downloads/AoT_Chicago.complete.2018-06-19 -t 30m```

Typing ```-h``` or ```--help``` when using this tool will pull up the help: ```python3 movingAvg.py -h```.

Errors will be specified for user error such as: not specifying the units of the period, not specifying an input file, etc.

### Compatibility
This tool was tested on a desktop computer with an Intel(R) Core(TM) i5-3470 CPU @ 3.20GHz, 8 GB of RAM, Ubuntu 18.04 LTS, and Linux 4.15.0-23-generic. It has also been tested on an Apple Macbook and worked correctly.
