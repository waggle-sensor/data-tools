# movingAvg.py
# takes in a .csv, makes moving averages of sensor data, writes out a .csv
# for a more detailed explanation, see README.md

from collections import OrderedDict
from datetime import timedelta
from collections import deque
import argparse
import datetime
import time
import csv
import os
import re

def setup():
        
    global inputFile
    global outputFile
    global period
    
    #set up command line arguments
    parser = argparse.ArgumentParser(description="make moving averages and produce .csv file data sets from data.csv.gz")
    parser.add_argument('-i','--input', dest='input', help='input .csv file name')
    parser.add_argument('-t','--time', dest='period', help="moving average period. Type an int followed by 's','m','h',or 'd'.")
    parser.add_argument('-o','--output', dest='output', help='output .csv file name')
    args = parser.parse_args()

    #make sure user specifies an input .csv file and that it exists
    if args.input == None:
        print("Error: No input file given.")
        exit(1)
    elif not re.match(r".*.csv$|.*.csv $",args.input):
        print("Error: Input file must be .csv.")
        exit(1)
        
    if  not (os.path.exists(args.input)):
        print("Error: Input file does not exist.")
        exit(1)

    inputFile = args.input

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

    #make sure user specifies an output .csv file (does not need to exist; python will create it if it doesn't exist)
    if args.output is None:
        print("Error: No output file given.")
        exit(1)
    elif not re.match(r".*.csv$|.*.csv $",args.output):
        print("Error: Output file must be .csv.")
        exit(1)

    outputFile = args.output

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

                for i in range(0,len(fieldNames)):
                    if 'value_hrf' not in fieldNames[i] and 'value_raw' not in fieldNames[i]:
                        header = header + fieldNames[i] + ','

                header = header + 'sum,count,SMA\n'
                oFile.write(header)

            #save the timestamp and value_hrf, then delete these and value_raw from the current row
            #(value_raw will most likely not be used by the end user and does not make sense to keep track of)
            timestamp = row['timestamp']
            value_hrf = row['value_hrf']
            del row['timestamp'], row['value_hrf'], row['value_raw']

            #iterate through the items in the row dictionary to build the key for the sensorDict
            for k,v in row.items():
                sensorKey = sensorKey + v + ','

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
                #format is: node_id,subsystem,sensor,parameter,sum,count,SMA

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

    #end timer and show run time
    timerEnd = time.time()
    runTime = timerEnd-timerStart
    print("Done. ",end="")
    print("Took %.2fs to complete." % runTime)
