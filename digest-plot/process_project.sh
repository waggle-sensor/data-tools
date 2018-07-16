./stage_project.sh $1
find ./scratch -name $1.complete.[1-9]* | xargs -n 1 sh -c './create_project_graphs.sh $0'
find ./scratch -name $1.complete.[1-9]* | xargs -n 1 sh -c 'python3 gen_tables.py $0'
mkdir -p ./build/plots
mkdir -p ./build/tables
# rm -rf ./build/plots/*
# rm -rf ./build/tables/*
if [ $(find ./scratch -name *.png | wc -l ) -gt 0 ]; then
	echo "Moving files"
	mv $(find ./scratch -name *.png) ./build/plots
fi 

if [ $(find ./scratch -name *.html | wc -l ) -gt 0 ]; then
	echo "Moving files"
	mv $(find ./scratch -name *.html) ./build/tables
fi 
cp $(find ./scratch -name style.css | head -1) ./build/tables
cat $(find ./scratch/$1.complete.[1-9]* -name nodes.csv) | awk 'NR==1 || !/node_id,project_id,vsn,address,lat,lon,description/' > scratch/nodes.csv
mv ./scratch/nodes.csv ./build/$1_nodes.csv

#python3 build-index ./scratch/nodes.csv ./build
