#!/bin/bash
#This bash script will reduce the full data set, output a new reduced data set, and archive the new data set with the 
#provenance, nodes, sensors .csv files, and the README.md file.

if ! python3 dataReduction.py -i data.csv -t "$1" -o reducedData.csv; then
	exit 1
fi

if [ ! -f reducedData.csv ] || [ ! -f nodes.csv ] || [ ! -f README.md ] || [ ! -f sensors.csv ] || [ ! -f provenance.csv ]; then
	echo "Files missing. Aborting."
	echo "Please ensure reducedData.csv, nodes.csv, README.md, sensors.csv, and provenance.csv are present."
	exit 1
fi

touch reducedREADME.md
> reducedREADME.md

echo "## NOTE: This README has been modifed by dataReduction.sh, and the data included in this file is now reduced. " >> reducedREADME.md
echo "Within this file, the 'data.csv.gz' file is often referred to as the compressed CSV containing the sensor data. This has been replaced by the file reducedData.csv." >> reducedREADME.md
echo "All other metadata mentioned in this README remains the same, except for the provenance metadata. The new provenance is listed here." >> reducedREADME.md
echo "New Provenance - This data was reduced and combined with the original digest metadata on " >> reducedREADME.md
echo `date +%Y-%m-%d` >> reducedREADME.md

cat README.md >> reducedREADME.md

echo "Archiving..."

if tar cvzf reducedDataSet.tar.gz reducedData.csv nodes.csv reducedREADME.md sensors.csv provenance.csv; then
	echo "Done."
else
	echo "Error: It is possible that not all files to be archived are present, or some other error occurred."
fi

rm reducedREADME.md
rm reducedData.csv