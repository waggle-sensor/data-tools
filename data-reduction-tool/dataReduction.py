# dataReduction.py
# currently takes in a .csv file and reads it
# parses through the large csv data set and reduces the amount of data
# by averaging/combining pieces of data over a certain time period given in seconds
# writes out CSV file. 

from collections import OrderedDict
from datetime import timedelta
import argparse
import datetime
import time
import csv
import io
import os
import re

def setup():
    
    global inputFile
    global outputFile
    global period
    global printLines
    global lines
    
    #set up command line arguments
    parser = argparse.ArgumentParser(description="average and reduce .csv file data sets from data.csv.gz")
    parser.add_argument('-i','--input', dest='input', help='Input .csv file name.')
    parser.add_argument('-t','--time', dest='period', help="Rows condense over this amt of time. Type an int followed by 's','m','h',or 'd'.")
    parser.add_argument('-o','--output', dest='output', help='Output .csv file name.')
    parser.add_argument('-v','--verbose', dest='numLines', help='Type an int. Prints # of lines parsed for every increment of entered int.')
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

    if args.numLines is not None:
        printLines = True
        try:
            lines = int(args.numLines)
        except ValueError:
            print("Error: Verbose option input must be an integer.")
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
    
    global inputFile
    global fieldNames
    global outputDict
    global period
    global minmax
    global beginMinMaxCalcs
    global printLines
    global lines
    
    valStr = ''
    count = 0
    newVal = ''
    currMax = 0
    currMin = 0

    timeRange = {"beginTime":0,"endTime":0}
    
    with open(inputFile, "r") as file:

        #create a csv reader object (it is an Ordered Dictionary of all the rows from the .csv file)
        #populate the fieldNames variable to place at the top of the output .csv file
        #replace any null values so that no errors occur
        reader = csv.DictReader(x.replace('\0', 'NullVal') for x in file)
        fieldNames = reader.fieldnames

        #go through each line of the input .csv file
        for row in reader:

            count = count + 1

            #print number of lines parsed every *lines* amount of lines
            if (printLines == True) and (count % lines == 0):
                print(count)

            #start the output evenly at the day, hour, or minute,
            if (count == 1):

                hours = int(row['timestamp'][11:13])
                minutes = int(row['timestamp'][14:16])
                seconds = int(row['timestamp'][17:])

                difference = hours*60*60 + minutes*60 + seconds
                
                timeRange["beginTime"] =  (datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()
                timeRange["beginTime"] = timeRange["beginTime"] - difference
                timeRange["endTime"] = timeRange["beginTime"] + period
                
            #set the new beginning and new end of the time range
            #if there is a gap in the data, this while loop runs until it hits the next timestamp
            while (timeRange["endTime"] < (datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()):
                timeRange["beginTime"] = timeRange["endTime"]
                timeRange["endTime"] = timeRange["endTime"] + period
                
            #create the temporary dictionary (uses each sensor's value_hrf as part of the value for each of the keys in outputDict) to hold
            #the sum, count, min, and max of the sensor hrf values over the specified time period
            newVal = row['value_hrf']
            temp = {'sum':newVal,'count':1, 'max':newVal, 'min':newVal}

            #delete value columns so that when getting all columns, they can just be used as the dict key
            #(value_raw will most likely not be used by end user and does not make sense to keep track of)
            del row['value_hrf'],row['value_raw']

            #iterate through the dictionary to generate the outputDict for each time period
            for k,v in row.items():

                #concatenate fields to be used as dictionary keys except value_hrf (to be used as part of dictionary values) and value_raw (deleted)
                #edit timestamp (to be used as part of dictionary keys - this is what determines how many rows from the input .csv file will be condensed into one row)
                #timestamp adjusted based on timeRange from code above generated by user input - timestamp is also halfway between the previous period and next period
                if k == 'timestamp':
                    valStr = valStr + str(datetime.datetime.utcfromtimestamp(timeRange["endTime"] - period/2).strftime('%Y/%m/%d %H:%M:%S'))
                else:
                    valStr = valStr + ',' + v

            #if the key already exists (meaning the row has already been made and now the current value_hrf just needs to be added to the sum and the count value needs to be incremented)
            #then try to set the value of the dictionary key (key is in the format: timestamp,node_id,subsystem,sensor,parameter) - skips any values that are 'NA' or are a mix of letters and numbers
            #dictionary value is another dictionary in the format: {'sum':sum,'count':count,'min':min,'max':max}
            #else just update the outputDict with the temporary dictionary created above that contains the first value_hrf for the current key
            if valStr in outputDict:
                
                try:
                    #calculate min and max
                    currMax = max(float(newVal),float(outputDict[valStr]['max']))
                    currMin = min(float(newVal),float(outputDict[valStr]['min']))
                        
                    outputDict[valStr] = {'sum':str(float(outputDict[valStr]['sum'])+float(temp['sum'])),'count':outputDict[valStr]['count']+1,'min':currMin,'max':currMax}

                    #if there are more than *beginMinMaxCalcs* values in the averaging period, add min and max to output file
                    if float(outputDict[valStr]['count']) > beginMinMaxCalcs:
                        minmax = True
                except ValueError:
                    pass
            else:
                outputDict[valStr] = temp

            valStr = ''

def writeFile():
    
    global outputFile
    global fieldNames
    global outputDict
    global minmax
    
    #erase whatever is currently in output csv file
    open(outputFile,'w').close()

    #now should have a dictionary with key value pairs in the following format (keys are shown as their titles but in the actual dictionary are the actual values):
    #{'timestamp,node_id,subsystem,sensor,parameter':{'sum':sum,'count':count}} or {'timestamp,node_id,subsystem,sensor,parameter':{'sum':sum,'count':count,'min':min,'max':max}}

    #update the output csv file's first line with the field names (removing 'value_hrf' and 'value_raw') in the following format:
    #timestamp,node_id,subsystem,sensor,parameter,sum,count,average or timestamp,node_id,subsystem,sensor,parameter,sum,count,average,min,max
    with open (outputFile,'w') as f:
        fieldNames.remove('value_raw')
        fieldNames.remove('value_hrf')

        for i in range(0,len(fieldNames)):
            f.write(str(fieldNames[i])+',')

        #if there are more than *beginMinMaxCalcs* values in the averaging period, add min and max to output file
        if minmax == True:
            f.write('sum,count,average,min,max\n')
        else:
            f.write('sum,count,average\n')

    #create the final output file
    with open (outputFile,'a') as f:

        #for each item in the dictionary - calculate the average of each time period (row) using the sum and count
        #include the average in the value dictionary of outputDict
        for key,val in outputDict.items():
            try:
                val.update({'average':round(float(val['sum'])/val['count'],2)})
            except ValueError:
                val.update({'average':0})

            #write the whole row with the outputDict key (timestamp,node_id,subsystem,sensor,parameter) and the outputDict values (sum,count,average,max,min)
            #also include the average, max, and min if there are more than *beginMinMaxCalcs* values in the averaging period
            if minmax == True:    
                f.write(str(key)+','+str(val['sum'])+','+str(val['count'])+','+str(val['average'])+','+str(val['min'])+','+str(val['max'])+'\n')
            else:
                f.write(str(key)+','+str(val['sum'])+','+str(val['count'])+','+str(val['average'])+'\n')
            
if __name__ == "__main__":
    
    #variable instantiations
    global inputFile
    global outputFile
    global fieldNames
    global outputDict
    global period
    global minmax
    global beginMinMaxCalcs
    global printLines
    global lines

    inputFile = ''
    outputFile = ''
    fieldNames = []
    outputDict = OrderedDict()
    period = 0
    minmax = False
    beginMinMaxCalcs = 1000
    printLines = False
    lines = 0

    #begin generating data
    print("Generating...")

    #begin timer for benchmarking
    timerStart = time.time()

    #get user input, reduce and store data, write new .csv file
    setup()
    createData()
    writeFile()

    #end timer and show run time
    timerEnd = time.time()
    runTime = timerEnd-timerStart
    print("Done. ",end="")
    print("Took %.2fs to complete." % runTime)
