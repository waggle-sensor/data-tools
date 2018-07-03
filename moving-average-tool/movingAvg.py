# movingAvg.py
# takes in a .csv and makes moving averages of sensor data
# Creates an output CSV file that is stored with other metadata inside a created directory. 

from collections import OrderedDict
from datetime import timedelta
from collections import deque
import subprocess
import argparse
import datetime
import shutil
import errno
import time
import csv
import os
import re

def setup():
        
    global inputFile
    global outputFile
    global period
    global dirPath
    global subDir
    
    #set up command line arguments
    parser = argparse.ArgumentParser(description="make moving averages and produce .csv file data sets from data.csv.gz")
    parser.add_argument('-i','--input', dest='path', help="Path to unpackaged complete node data set (e.g. '-i /home/name/AoT_Chicago.complete.2018-06-19').")
    parser.add_argument('-t','--time', dest='period', help="Moving average period. Type an int followed by 's','m','h',or 'd' (e.g. '-t 30m').")
    args = parser.parse_args()

    #check that path exists and contains the necessary files
    if os.path.exists(args.path):
        dirPath = str(args.path)
        if not os.path.isfile(str(dirPath+"/data.csv")) or not os.path.isfile(str(dirPath+"/nodes.csv")) or not os.path.isfile(str(dirPath+"/sensors.csv")) or not os.path.isfile(str(dirPath+"/provenance.csv")) or not os.path.isfile(str(dirPath+"/README.md")):
            print("Error: Files missing from input directory path.")
            exit(1)
    else:
        print("Error: Path does not exist. Specify full path to unpackaged complete node data set")
        exit(1);

    #remove trailing slash if user includes it
    if (str(dirPath[-1:]) == "/"):
        dirPath = dirPath[:-1]
        
    #set the input file (full path to file) 
    inputFile = dirPath+"/data.csv"

    #make sure user specifies a time period
    if args.period == None:
        print("Error: No time value given. Must be an int followed by 's','m','h',or 'd'.")
        exit(1)

    if not re.match(r"[0-9]+[s,m,h,d]{1}$| [0-9]+[s,m,h,d]{1}$|[0-9]+[s,m,h,d]{1} $| [0-9]+[s,m,h,d]{1} $",args.period):
        print("Error: Time value must be an int followed by 's','m','h',or 'd'.")
        exit(1)

    interval = args.period[-1:]
    numInterval = abs(int(args.period[0:-1]))

    if (numInterval < 1):
        print("Error: Time value must be a positive integer greater than 0.")
        exit(1)

    #convert user input time period into seconds - must be at least 24 seconds
    if interval == 's':
        if(numInterval < 24):
            print("Error: Time value cannot be less than 24 seconds.")
            exit(1)
        else:
            period = numInterval
    elif interval == 'm':
        period = numInterval*60
    elif interval == 'h':
        period = numInterval*60*60
    elif interval == 'd':
        period = numInterval*24*60*60
    else:
        period = numInterval

    if period > 172800:
        print("Error: Time interval must be less than 2 days.")
        exit(1)

    #create the sub directory that will contain the moving averaged data and the copied metadata files
    dirList = dirPath.split("/")
    parentDir = dirList[len(dirList)-1]
    subDir = dirPath + "/" + parentDir + "_moving_average_data_" + str(args.period)
    fileName = subDir + "/data.csv"
    
    if not os.path.exists(os.path.dirname(fileName)):
        try:
            os.makedirs(os.path.dirname(fileName))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    #set the output file (full path to file)
    outputFile = fileName

def createData():
    
    global fieldNames
    global inputFile
    global outputFile
    global period
    
    sensorDict = {}
    sensorKey = ''
    beginOutputCount = 1
    count = 0
    summation = 0
    avg = 0
    timeRange = {"beginTime":"","endTime":""}
    setBeginCount = 0
    header = ''
    currKey = ''
    hrfTitle = ''
    
    open(outputFile,'w').close()
        
    with open(inputFile, 'r') as iFile, open(outputFile,'a') as oFile:
                
        #create a csv reader object (it is an Ordered Dictionary of all the rows from the .csv file)
        #populate the fieldNames variable to place at the top of the output .csv file
        #replace any null values so that no errors occur
        reader = csv.DictReader(x.replace('\0', 'NullVal') for x in iFile)
        fieldNames = reader.fieldnames

        #go through each line of the input .csv file
        for row in reader:
            
            #set the first timestamp as the start point for the first period
            #also write out the field names to the output file
            setBeginCount = setBeginCount + 1
            if (setBeginCount == 1):
                
                timeRange["endTime"] =  (datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()
                timeRange["beginTime"] = timeRange["endTime"] - period

                #sensor values can come from the original data set or the data reduction tool; otherwise, the tool cannot function
                for i in range(0,len(fieldNames)):
                    if 'value_hrf' not in fieldNames[i] and 'value_raw' not in fieldNames[i] and 'value_hrf_average' not in fieldNames[i]:
                        header = header + fieldNames[i] + ','
                        
                    if (fieldNames[i] == "value_hrf"):
                        hrfTitle = "value_hrf"
                    elif (fieldNames[i] == "value_hrf_average"):
                        hrfTitle = "value_hrf_average"

                if (hrfTitle != "value_hrf" and hrfTitle != "value_hrf_average"):
                    print("Error: Could not find appropriate value header. CSV file headers must include either 'value_hrf' or 'value_hrf_average'.")
                    exit(1)


                header = header + 'value_hrf_sum,value_hrf_count,value_hrf_moving_average\n'
                oFile.write(header)

            #save the timestamp and value_hrf (or value_hrf_average), then delete these and value_raw from the current row
            #(value_raw will most likely not be used by the end user and does not make sense to keep track of)
            timestamp = row['timestamp']
            value_hrf = row[hrfTitle]
            del row['timestamp'], row[hrfTitle]

            #delete the value_raw column if it exists
            try:
                del row['value_raw']
            except:
                pass

            #iterate through the items in the row dictionary to build the key for the sensorDict
            for k,v in row.items():
                sensorKey = sensorKey + str(v) + ','

            #Take off last comma
            sensorKey = sensorKey[:-1]

            #if the current node/sensor (key) has already been added to the dictionary, then start appending new values
            #and calculating moving averages
            #else, increment number of sensors and make a new dictionary key:value pair with the key being the current node/sensor and
            #the value being a deque that contains lists of the sensor values and their timestamps
            if sensorKey in sensorDict:

                #add next node/sensor value to the deque
                sensorDict[sensorKey].append([value_hrf,timestamp])

                #if the incoming node/sensor timestamp is greater than or equal to the end of the current time range, set the new end of the time range to that timestamp
                #and set the new beginning of the time range to the new timestamp minus the period
                if (datetime.datetime.strptime(timestamp,'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds() >= timeRange["endTime"]:
                    timeRange["endTime"] = (datetime.datetime.strptime(timestamp,'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()
                    timeRange["beginTime"] = (datetime.datetime.strptime(timestamp,'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds() - period

                    #begin popping items off of the left side of the deque and do this until the only items in the
                    #deque are ones where the timestamps are in the time range
                    nextInQueue = sensorDict[sensorKey].popleft()
                    nextTimestamp = (datetime.datetime.strptime(nextInQueue[1],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()
                    
                    while nextTimestamp < timeRange["beginTime"]:
                        nextInQueue = sensorDict[sensorKey].popleft() 
                        nextTimestamp = (datetime.datetime.strptime(nextInQueue[1],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()

                    #re-append the last value since the while loop goes one removal too far
                    sensorDict[sensorKey].appendleft(nextInQueue)
                    #if sensorKey == '001e0610ba46,lightsense,apds_9006_020,intensity':
                        #print(sensorDict[sensorKey])

                #calculate the moving average for the current period by taking a simple moving average of
                #all the values in the deque of the current node/sensor (specified by the sensorKey)
                #ignore values that are not numbers (e.g. 'NA') or are a mix of letters and numbers (such as an ID)
                #these values are instead just put in place of the avg
                for x in sensorDict[sensorKey]:
                    try:
                        avg = avg + float(x[0]) #x[0] since the first item in the two-item list is the value; x[1] is the timestamp
                        count = count + 1
                    except:
                        avg = x[0]
                        
                summation = avg

                try:
                    avg = summation/float(count)
                except TypeError:
                    pass

                #fill in the the output file
                #format is: node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_moving_average
                #timestamps are written out as halfway between the beginning and end of the current time range
                currKey = str(datetime.datetime.utcfromtimestamp(timeRange["endTime"] - period/2).strftime('%Y/%m/%d %H:%M:%S'))+',' + sensorKey

                #write out current entry to output file
                oFile.write(currKey + ',' + str(summation) + ',' + str(count) + ',' + str(avg) + '\n')
            else:
                #increment the number of sensors and add a new key:value pair to the sensor dictionary that contains a deque with the first
                #sensor value/timestamp for that node/sensor
                sensorDict[sensorKey] = deque()
                sensorDict[sensorKey].append([value_hrf,timestamp])

            #reset average variables and sensorKey for next calculation
            avg = 0
            sensorKey = ""
            summation = 0
            count = 0

def copyDigestFiles():
    
    global dirPath
    global subDir

    #copy the metadata files that are from the parent directory
    try:
        shutil.copyfile(dirPath+"/nodes.csv",subDir+"/nodes.csv",follow_symlinks=True)
        shutil.copyfile(dirPath+"/provenance.csv",subDir+"/provenance.csv",follow_symlinks=True)
        shutil.copyfile(dirPath+"/sensors.csv",subDir+"/sensors.csv",follow_symlinks=True)
        shutil.copyfile(dirPath+"/README.md",subDir+"/README.md",follow_symlinks=True)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

    #modify the README, create new README, delete old README
    modifierText = """## NOTE: This README has been modifed by movingAvg.py, and the data included in this directory now contains moving averages of node/sensor data.\n
Within this README, the 'data.csv.gz' archive is referred to as the compressed CSV containing the sensor data file (data.csv). The data.csv file from this compressed archive has been replaced by the moving averaged data.csv.
All other metadata mentioned in this README remains the same, except for the provenance metadata and the list of columns in data.csv.gz. Since this file no longer exists, these columns are incorrect.
The columns remain the same but 'value_raw' and 'value_hrf' do not exist in the new moving averaged data.csv file; instead, the columns now include 'value_hrf_sum,value_hrf_count,value_hrf_moving_average'
The provenance.csv file contains the provenance for the original data set. Provenance for moving averaged data:
New Provenance - This moving averaged data was created and combined with the original digest metadata on """ + str(datetime.datetime.utcnow()) + ". It has been modifed by the movingAvg.py averaging tool.\n\n"

    newReadme = subDir + "/movingAveragedREADME.md"
    oldReadme = subDir+"/README.md"
    with open (newReadme,'w') as n, open (oldReadme, "r") as o:
        text = o.read()
        n.write(modifierText+text)

    try:
        subprocess.run(["rm " + oldReadme.replace(" ","\ ")], shell=True, check=True)
        subprocess.run(["mv " + newReadme.replace(" ","\ ") + " README.md" ], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

if __name__ == "__main__":

    #variable instantiations
    global inputFile
    global outputFile
    global fieldNames
    global period

    inputFile = ''
    outputFile = ''
    fieldNames = []
    period = 0
    
    #start timer and begin generating data
    print("Generating...")
    timerStart = time.time()

    #get user input, calculate and store data, write new .csv file
    setup()
    createData()
    copyDigestFiles()

    #end timer and show run time
    timerEnd = time.time()
    runTime = timerEnd-timerStart
    print("Done. ",end="")
    print("Took %.2fs to complete." % runTime)
