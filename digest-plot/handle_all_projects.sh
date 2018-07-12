#!/bin/bash
rm -rf ./scratch/*.latest.tar
rm -rf ./scratch/*.complete.[1-9]*
curl "http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/index.php" | tr "<" "\n" | grep latest.tar | cut -d ">" -f 1 | sed "s/a href='.//g" | sed "s/.[a-z]*.latest.tar'//g" | sed 's/\///g' | xargs -n 1 sh -c './stage_project.sh $0'
find ./scratch -name *.complete.[1-9]* | xargs -n 1 sh -c './create_project_graphs.sh $0'
find ./scratch -name *.complete.[1-9]* | xargs -n 1 sh -c 'python3 gen_tables.py $0'
if [ ! -d ./scratch/plots ]; then
	mkdir ./scratch/plots
fi
if [ ! -d ./scratch/tables ]; then
	mkdir ./scratch/tables
fi
rm -rf ./scratch/plots/*
rm -rf ./scratch/tables/*
mv $(find ./scratch -name *.png) ./scratch/plots
mv $(find ./scratch -name *.html) ./scratch/tables
cp $(find ./scratch -name style.css | head -1) ./scratch/tables
