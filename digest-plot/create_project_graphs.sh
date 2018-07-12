#!/bin/bash

usage() {
	echo "usage: ${0} project_dir_path"
}

if [ "$1" = "" ]; then
	usage
	exit 1
fi

if [ ! -d scratch ]; then
	mkdir scratch
fi

project_dir="${1%/}"
if [ ! -d "$project_dir" ]; then
	echo "[ERROR] $project_dir does not exist"
	exit 1
fi

for file in "data.csv.gz" "offsets.csv" "nodes.csv" "sensors.csv"; do
	if [ ! -f "$project_dir/$file" ]; then
		echo "[ERROR] $file does not exist"
		exit 1
	fi
done

for ((i=1;i<=30;i++)); do
	date=$(date -u -d "$i days ago" +%Y-%m-%d)
	python3 ../slice-date-range/slice-date-range.py "$project_dir" "$date" "$date"
	date_dir="$project_dir".from-"$date"-to-"$date"
	data_path="$date_dir"/data.csv.gz
	gzip -d "$data_path"
	python3 extract_nodes.py "$project_dir" "$date_dir" "$date"
done

date=$(date -u -d "1 days ago" +%Y-%m-%d)
data_column=$(head -n1 "${project_dir}".from-"${date}"-to-"${date}"/data.csv | tr "," "\n" | grep -nx "value_hrf\|value_hrf_average\|value_hrf_moving_average" |  cut -d":" -f1)

rm -rf "$project_dir".from*

python3 gen_digest_plots.py "$project_dir" "$data_column"

rm -rf "$project_dir"/data
rm graph.plt
