#!/bin/bash
rm -rf ./scratch/*.latest.tar
rm -rf ./scratch/*.complete.[1-9]*
curl "http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php" | tr "<" "\n" | grep complete.latest.tar | cut -d ">" -f 1 | sed "s/a href='.//g" | sed "s/.[a-z]*.latest.tar'//g" | sed 's/\///g' | xargs -n 1 sh -c './stage_project.sh $0'
find ./scratch -name *.complete.[1-9]* | xargs -n 1 sh -c './create_project_graphs.sh $0'
find ./scratch -name *.complete.[1-9]* | xargs -n 1 sh -c 'python3 gen_tables.py $0'
mkdir -p ./build/plots
mkdir -p ./build/tables
rm -rf ./build/plots/*
rm -rf ./build/tables/*
mv $(find ./scratch -name *.png) ./build/plots
mv $(find ./scratch -name *.html) ./build/tables
cp $(find ./scratch -name style.css | head -1) ./build/tables

cat $(find ./scratch -name nodes.csv) | awk 'NR==1 || !/node_id,project_id,vsn,address,lat,lon,description/' > scratch/nodes.csv
python3 build-index ./scratch/nodes.csv ./build
