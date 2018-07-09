#!/bin/bash

usage() {
	echo "usage: extract [[[-p PATTERN] [-i INPUT] [-o OUTPUT] [-v INVERT] [-a AND]] | [-h]]"
}

set -e

pattern=

while [ "$1" != "" ]; do
	case $1 in
		-p | --pattern )	shift
							pattern=$1
							;;
		-i | --input )		shift
							input=$1
							;;
		-o | --output )		shift
							output=$1
							;;
		-v | --invert )		shift
							invert=$1
							;;
		-a | --and )		shift
							and=$1
							;;
		-h | --help )		usage
							exit
							;;
		* )					usage
							exit 1
	esac
	shift
done

if [ "$invert" = "True" -a "$and" = "True" ]; then
	grep -E "${pattern}" -a -v -w $input > $output
elif [ "$invert" = "True" ]; then
	grep "${pattern}" -a -v -w $input > $output
elif [ "$and" = "True" ]; then
	grep -E "${pattern}" -a $input > $output
else
	grep "${pattern}" -a $input > $output
fi

