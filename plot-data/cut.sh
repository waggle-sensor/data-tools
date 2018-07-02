#!/bin/bash

usage() {
	echo "usage: extract [[[-d DELIMITER] [-f FIELDS] [-i INPUT] [-o OUTPUT]] | [-h]]"
}

set -e

while [ "$1" != "" ]; do
	case $1 in
		-d | --delimiter )	
							shift
							delimiter=$1
							;;
		-f | --fields )	
							shift
							fields=$1
							;;
		-i | --input )		
							shift
							input=$1
							;;
		-o | --output )		
							shift
							output=$1
							;;
		-h | --help )		
							usage
							exit
							;;
		* )					
							usage
							exit 1
	esac
	shift
done

if [ "$input" = "$output" ]; then
	mv $input "${input}.old"
	cut -d "${delimiter}" -f "${fields}" < "${input}.old" > $output &&
	rm "${input}.old"
else
	cut -d "${delimiter}" -f "${fields}" $input > $output
fi
