#!/bin/bash
set -e
rm -rf ./scratch/*.latest.tar
rm -rf ./scratch/*.complete.[1-9]*
rm -rf ./build/plots/*
rm -rf ./build/tables/*
rm -rf ./build/data_dates/*
curl "http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php" | \
	tr "<" "\n" | grep complete.latest.tar | cut -d ">" -f 1 | sed "s/a href='.//g" | sed "s/.[a-z]*.latest.tar'//g" | sed 's/\///g' | xargs -n 1 sh -c './process_project.sh $0'
echo "node_id,project_id,vsn,address,lat,lon,description" > ./build/nodes.csv
cat ./build/*_nodes.csv | grep -v "node_id" >> ./build/nodes.csv 
python3 build-index ./build/nodes.csv ./build

