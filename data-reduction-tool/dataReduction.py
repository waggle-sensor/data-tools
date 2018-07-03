# dataReduction.py
# Takes in a .csv file and reads it.
# Parses through the large csv data set and reduces the amount of data
# by averaging/combining pieces of data over a certain time period.
# Creates an output CSV file that is stored with other metadata inside a created directory. 

from collections import OrderedDict
from datetime import timedelta
import subprocess
import argparse
import datetime
import shutil
import errno
import time
import csv
import io
import os
import re


def setup():
    
    global inputFile
    global outputFile
    global dirPath
    global subDir
    global period
    global printLines
    global lines
    
    #set up command line arguments
    parser = argparse.ArgumentParser(description="average and reduce .csv file data sets from data.csv.gz")
    parser.add_argument('-i','--input', dest='path', help="Path to unpackaged complete node data set. (e.g. '-i /home/name/AoT_Chicago.complete.2018-06-19')")
    parser.add_argument('-t','--time', dest='period', help="Rows condense over this amt of time. Type an int followed by 's','m','h',or 'd' (e.g. '-t 30m').")
    parser.add_argument('-v','--verbose', dest='numLines', help="Type an int. Prints # of lines parsed for every increment of entered int (e.g. '-v 1000').")
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

    #make sure verbose option (when included) includes an integer with it
    if args.numLines is not None:
        printLines = True
        try:
            lines = int(args.numLines)
        except ValueError:
            print("Error: Verbose option input must be an integer.")
            exit(1)

    #create the sub directory that will contain the reduced data and the copied metadata files
    dirList = dirPath.split("/")
    parentDir = dirList[len(dirList)-1]
    subDir = dirPath + "/" + parentDir + "_reduced_data_" + str(args.period)
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
    
    global inputFile
    global fieldNames
    global outputDict
    global period
    global minmax
    global beginMinMaxCalcs
    global printLines
    global lines
    global hrfTitle
    
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

        #sensor values can come from the original data set or the moving average tool; otherwise, the tool cannot function
        for i in range(0,len(fieldNames)):
            if (fieldNames[i] == "value_hrf"):
                hrfTitle = "value_hrf"
            elif (fieldNames[i] == "value_hrf_moving_average"):
                hrfTitle = "value_hrf_moving_average"

        if (hrfTitle != "value_hrf" and hrfTitle != "value_hrf_moving_average"):
            print("Error: Could not find appropriate value header. CSV file headers must include either 'value_hrf' or 'value_hrf_moving_average'.")
            exit(1)

        #go through each line of the input .csv file
        for row in reader:

            count = count + 1

            #print number of lines parsed every *lines* amount of lines
            if (printLines == True) and (count % lines == 0):
                print(count)

            #start the output evenly at the day, hour, or minute,
            if (count == 1):
                
                hours = int(datetime.datetime.strptime(row['timestamp'], '%Y/%m/%d %H:%M:%S').hour)
                minutes = int(datetime.datetime.strptime(row['timestamp'], '%Y/%m/%d %H:%M:%S').minute)
                seconds = int(datetime.datetime.strptime(row['timestamp'], '%Y/%m/%d %H:%M:%S').second)

                difference = hours*60*60 + minutes*60 + seconds
                
                timeRange["beginTime"] =  (datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()
                timeRange["beginTime"] = timeRange["beginTime"] - difference
                timeRange["endTime"] = timeRange["beginTime"] + period
                
            #set the new beginning and new end of the time range
            #if there is a gap in the data, this while loop runs until it hits the next timestamp
            while (timeRange["endTime"] < (datetime.datetime.strptime(row['timestamp'],'%Y/%m/%d %H:%M:%S') - datetime.datetime(1970,1,1)).total_seconds()):
                timeRange["beginTime"] = timeRange["endTime"]
                timeRange["endTime"] = timeRange["endTime"] + period
                
            #create the temporary dictionary (uses each sensor's value_hrf (or value_hrf_moving_average) as part of the value for each of the keys in outputDict) to hold
            #the sum, count, min, and max of the sensor hrf values over the specified time period
            newVal = row[hrfTitle]
            temp = {'sum':newVal,'count':1, 'max':newVal, 'min':newVal}

            #delete value columns so that when getting all columns, they can just be used as the dict key
            #(value_raw will most likely not be used by end user and does not make sense to keep track of)
            del row[hrfTitle]

            #delete the value_raw column if it exists
            try:
                del row['value_raw']
            except:
                pass

            #iterate through the dictionary to generate the outputDict for each time period
            for k,v in row.items():

                #concatenate fields to be used as dictionary keys except value_hrf (or value_hrf_moving_average) (to be used as part of dictionary values) and value_raw (deleted)
                #edit timestamp (to be used as part of dictionary keys - this is what determines how many rows from the input .csv file will be condensed into one row)
                #timestamp adjusted based on timeRange from code above generated by user input - timestamp is also halfway between the previous period and next period
                if k == 'timestamp':
                    valStr = valStr + str(datetime.datetime.utcfromtimestamp(timeRange["endTime"] - period/2).strftime('%Y/%m/%d %H:%M:%S'))
                else:
                    valStr = valStr + ',' + str(v)

            #if the key already exists (meaning the row has already been made and now the current value_hrf (or value_hrf_moving_average) just needs to be added to the sum and the count value needs to be incremented)
            #then try to set the value of the dictionary key (key is in the format: timestamp,node_id,subsystem,sensor,parameter) - skips any values that are 'NA' or are a mix of letters and numbers
            #dictionary value is another dictionary in the format: {'sum':sum,'count':count,'min':min,'max':max}
            #else just update the outputDict with the temporary dictionary created above that contains the first value_hrf(or value_hrf_moving_average) for the current key
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
    global dirPath
    global hrfTitle
    
    #erase whatever is currently in output csv file
    open(outputFile,'w').close()

    #now should have a dictionary with key value pairs in the following format (keys are shown as their titles but in the actual dictionary are the actual values):
    #{'timestamp,node_id,subsystem,sensor,parameter':{'sum':sum,'count':count,'min':min,'max':max}}

    #update the output csv file's first line with the field names (removing 'value_hrf' (or 'value_hrf_moving_average') and 'value_raw') in the following format:
    #timestamp,node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_average or timestamp,node_id,subsystem,sensor,parameter,value_hrf_sum,value_hrf_count,value_hrf_average,value_hrf_min,value_hrf_max
    with open (outputFile,'w') as f:
        #delete the value_raw column if it exists
        try:
            fieldNames.remove('value_raw')
        except:
            pass
        
        fieldNames.remove(hrfTitle)

        for i in range(0,len(fieldNames)):
            f.write(str(fieldNames[i])+',')

        #if there are more than *beginMinMaxCalcs* values in the averaging period, add min and max to output file
        if minmax == True:
            f.write('value_hrf_sum,value_hrf_count,value_hrf_average,value_hrf_min,value_hrf_max\n')
        else:
            f.write('value_hrf_sum,value_hrf_count,value_hrf_average\n')

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
    modifierText = """## NOTE: This README has been modifed by dataReduction.py, and the data included in this directory is now reduced.\n
Within this README, the 'data.csv.gz' archive is referred to as the compressed CSV containing the sensor data file (data.csv). The data.csv file from this compressed archive has been replaced by the reduced data.csv.
All other metadata mentioned in this README remains the same, except for the provenance metadata and the list of columns in data.csv.gz. Since this file no longer exists, these columns are incorrect.
The columns remain the same but 'value_raw' and 'value_hrf' do not exist in the new reduced data.csv file; instead, the columns now include either 'value_hrf_sum,value_hrf_count,value_hrf_average', or 'value_hrf_sum,value_hrf_count,value_hrf_average,value_hrf_min,value_hrf_max'
The provenance.csv file contains the provenance for the original data set. Provenance for reduced data:
New Provenance - This data was reduced and combined with the original digest metadata on """ + str(datetime.datetime.utcnow()) + ". It has been modifed by the dataReduction.py data reduction tool.\n\n"

    newReadme = subDir + "/reducedREADME.md"
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
    global outputDict
    global period
    global minmax
    global beginMinMaxCalcs
    global printLines
    global lines
    global dirPath
    global subDir
    global hrfTitle

    inputFile = ''
    outputFile = ''
    fieldNames = []
    outputDict = OrderedDict()
    period = 0
    minmax = False
    beginMinMaxCalcs = 1000
    printLines = False
    lines = 0
    dirPath = ''
    subDir = ''
    hrfTitle = ''
    
    #begin generating data
    print("Generating...")

    #begin timer for benchmarking
    timerStart = time.time()

    #get user input, reduce and store data, write new .csv file
    setup()
    createData()
    writeFile()
    copyDigestFiles()

    #end timer and show run time
    timerEnd = time.time()
    runTime = timerEnd-timerStart
    print("Done. ",end="")
    print("Took %.2fs to complete." % runTime)
