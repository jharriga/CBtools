#!/usr/bin/python
#
# CBplot.py
# Reads COSbench CSV files and produces PNG file for each workstage
# Supports plot types of latency and throughput
# Uses 'argparse' to print help usage info
#########################################################

import sys
import os
import glob
import argparse
import datetime as dt
import csv
# Avoid "Could not open Display" error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as md

def plot_stats(theFile, plotType, key1, key2, yUnits):
#   theFile = the CSV file to be parsed
#   plotType = Avg-ResTime, Throughput, ...
#   key1 = start  column
#   key2 = end column
#   yUnits = units label, depends on plotType
#
    time = []
    clr = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
    ts_created = os.stat(theFile).st_ctime
    dt_created = dt.datetime.fromtimestamp(ts_created)
    print "PROCESSING - plotting Statistics:", plotType
    print "> Reading data from: {}".format(theFile)
    print "> File creation time: ", str(dt_created)

    with open(theFile,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
# Parse the first row looking for column locations
#   NOTE: for latency plot the key1 is 'Avg-ResTime'
#         for throughput plot the key1 is 'Throughput'
        header1 = plots.next()
        colIndex1 = header1.index(key1)
        colIndex2 = header1.index(key2)
# Read the second row which contains operation labels
        header2 = plots.next()
        opLabel = []
        for colNum in range(colIndex1, colIndex2, 1):
            opLabel.append(header2[colNum])
        numLabels=len(opLabel)
        print "> Operation Column range: ", colIndex1, colIndex2
        print "> Operation Count is: ", numLabels
        print "> Operations found: ", opLabel   # array of operation labels
# Initialize the opStats 2D array - holds table of statistics
#   2D array structure is opStats[opLabel#][row#]
##        opStats = [[], []]
        opStats = [[] for _ in range(numLabels)]
        totValue = []        # calculating average
# Make sure we have enough COLORS. One for each Operation
        numClrs = len(clr)
        if numLabels > numClrs:
            print "Too many operations %d. MAX of %d . Exiting", numLabels, numClrs
            sys.exit()
# Record the number of columns expected in every row
        numColumns = len(header2)
# NOW we are ready to read the actual statistics
        incrDay = int(0)        # increments timestamp on 24hr period
        rowCntr = int(0)        # outer loop counter - rows
        naCntr = int(0)         # counts number of ignored samples/rows
##        totValue = [0.0, 0.0, 0.0, 0.0]        # calculating average
# Initialize the array which contains averages
        for i in range (numLabels):
            totValue.append(float(0.0))

# Parse all the remaining rows
        for row in plots:
            cos_ts = dt.datetime.strptime(row[0],"%H:%M:%S")
            this = cos_ts.replace(year=dt_created.year, month=dt_created.month, day=dt_created.day)
            if (rowCntr > 0):               # check for day rollover 
                if (prev > this.hour):
                    incrDay += 1            # add a day
                    print ">* Adding a day at: ", str(this)
            date = this + dt.timedelta(days=incrDay)

# Ensure this row has the expected number of columns, otherwise skip it
            if len(row) == numColumns:
##                print "> rowCntr: ", str(rowCntr)   # DEBUG
                naFound = bool(False)    # records when N/A value is read
                for column in range(colIndex1, colIndex2, 1):
# Ignore/skip bad (or empty) sample rows
                    if row[column] == 'N/A':
                        naFound = bool(True)
                if naFound:
                    naCntr += 1
                    print "> Found N/A value, row number skipped: ", str(rowCntr)
                else:
# All values appear valid, proceed
                    time.append(date)
                    colCntr = int(0)       # inner loop counter - columns
                    for column in range(colIndex1, colIndex2, 1):
                        value = float(row[column])
                        opStats[colCntr].append(value)
                        totValue[colCntr] = totValue[colCntr] + value
                        colCntr += 1
            else:
                naCntr += 1
                print "> Incorrect numColumns, row number skipped: ", str(rowCntr)

            prev=this.hour
            rowCntr += 1

    xticks=len(time)                # number of samples
    print "> Number of valid time values: ", str(xticks)
    print "> Number of ignored/skipped row samples: ", str(naCntr)
    
    if xticks == 0:
        print "> No valid time values, no plot to generate"
        return

    fig = plt.figure(figsize=(18,7))
    ax1 = fig.add_subplot(111)
    plt.xticks(rotation=45)

# Plot the stats for each of the operation labels
    for x in range(0, numLabels, 1):
        thisAvg = round(float(totValue[x] / xticks), 2)
        labelStr = opLabel[x] + "=" + str(thisAvg)
##        ax1.plot(time, opStats[x], color=clr[x], linewidth=1, marker="o", label=opLabel[x])
        ax1.plot(time, opStats[x], color=clr[x], linewidth=1, marker="o", label=labelStr)

# Print the X and Y axis labels
    yType = str(plotType)
    yLabel = str(yType.upper()+yUnits)
    plt.ylabel(str(yLabel), fontsize=20)
    plt.xlabel('TIMESTAMP (%d samples)' % xticks, fontsize=20)
    # print the legend box (with color-coded operations)
    leg=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=19)
    plt.subplots_adjust(left=0.12,bottom=0.18, right=0.9, top=0.85, wspace=0.2,hspace=0.2)
# use the filename as the plot title
    plt.suptitle('%s '% theFile, fontsize=24)
# save the PDF - name convention is jobID_stagename.PDF
    basenm=os.path.basename(theFile)
# strips off the final "/" if its there
    pathnm=os.path.dirname(theFile)
# grab the tail of the path and prepend it to the PLOT fname   
    prepend=os.path.basename(pathnm)
    fname=prepend+'_'+basenm.split('.')[0]+'_'+plotType.upper()+'.png'
    plt.savefig(fname, format='png', dpi=1000)
    print('> Created PNG chart: '+fname)
#    fname=prepend+'_'+basenm.split('.')[0]+'_'+plotType.upper()+'.pdf'
#    plt.savefig(fname, format='pdf', dpi=1000)
#    print('> Created PDF chart: '+fname)
# END plot_stats Function

if __name__ == "__main__":

# check cmdline args
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir',help='Directory with COSbench csv files', required=True)
    parser.add_argument('-t','--type',help='type of plot (latency, throughput)', required=True)
    args = parser.parse_args()
# check if arg1 exists and is directory
    if os.path.isdir(args.dir) is False:
        print "No such Directory: ", args.dir 
        sys.exit()
# check if args.type specifies a valid plotType
    if args.type == 'latency':
# set up for plotting latency/ResponseTimes
        plot = "latency"
        colStart = "Avg-ResTime"
        colEnd = "Avg-ProcTime"
        units = " (ms)"
    elif args.type == 'throughput':
# set up for plotting Throughput
        plot = "throughput"
        colStart = "Throughput"
        colEnd = "Bandwidth"
        units = " (op/s)"
    else:
        print "Unsupported plot type requested:", args.type
        print "Supported types are: latency, throughput"
        sys.exit()
# Cmdline args look good
# Call the plotting function for CSV files found in the args.dir
#    exclude the CSV files which end with "-worker.csv"
#    and exclude results from 'init' stages since they are empty
    for file in list(glob.glob(args.dir+'/s?-*.csv')):
        if (file.find("-worker.csv") == -1) and (file.find("-init_") == -1):
            print "Plotting CSV file: ", file
            plot_stats(file, plot, colStart, colEnd, units)
        else:
            print "Skipping CSV file: ", file

# Wait for user input
#        os.system('read -s -n 1 -p "Press any key to continue..."')
#        print  

# END
