#!/bin/bash

usage() {
	echo "usage: ${0} project_id"
}

if [ "$1" = "" ]; then
	usage
	exit 1
fi
project_id=$1
wget "http://www.mcs.anl.gov/research/projects/waggle/downloads/datasets/${project_id}.complete.latest.tar" -P ./scratch
echo "File Downloaded"
tar -xf "scratch/${project_id}.complete.latest.tar" -C ./scratch
echo "File Untared"
