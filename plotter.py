#!/usr/bin/python
#
# plotter.py
# Reads COSbench CSV files and produces PDF file for each workstage
# Supports plot types of latency and throughput
# Uses 'argparse' to print help usage info
#########################################################

import sys
import os
import glob
import argparse
import datetime as dt
import csv
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
        print "> Operation Column range: ", colIndex1, colIndex2
        print "> Operations found: ", opLabel   # array of operation labels
# Initialize the opStats 2D array - holds table of statistics
#   2D array structure is opStats[opLabel#][row#]
        numLabels=len(opLabel)
        opStats = [[] for i in range(numLabels)]  
# Make sure we have enough COLORS. One for each Operation
        numClrs = len(clr)
        if numLabels > numClrs:
            print "Too many operations %d. MAX of %d . Exiting", numLabels, numClrs
            sys.exit()
# NOW we are ready to read the actual statistics
        incr = int(0)           # increments timestamp on 24hr period
        ocntr = int(0)          # outer loop counter
# parse all the remaining rows
        for row in plots:
            cos_ts = dt.datetime.strptime(row[0],"%H:%M:%S")
            this = cos_ts.replace(year=dt_created.year, month=dt_created.month, day=dt_created.day)
            if (ocntr > 0):                 # check for day rollover 
                if (prev > this.hour):
                    incr += 1               # add a day
                    print ">* Adding a day at: ", str(this)
            date = this + dt.timedelta(days=incr) 
            time.append(date)

            icntr = int(0)           # inner loop counter
            for column in range(colIndex1, colIndex2, 1):
                opStats[icntr].append(row[column])
                icntr += 1

            prev=this.hour
            ocntr += 1
    xticks=len(time)                # number of samples
    print "> Number of time values: ", str(xticks)

    fig = plt.figure(figsize=(18,6))
    ax1 = fig.add_subplot(111)
    ax1.yaxis.grid(True)
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.xaxis.grid(color='#CDCDC1', linestyle='-', linewidth=1)
    ax1.set_axisbelow(True)
# Add actual timestamp data on Xaxis
    xfmt=md.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
# Plot the stats for each of the operation labels
    for x in range(0, numLabels, 1):
        ax1.plot(time, opStats[x], color=clr[x], linewidth=1, marker="o", label=opLabel[x])
 
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)
# Print the X and Y axis labels
    yType = str(plotType)
    yLabel = str(yType.upper()+yUnits)
    plt.ylabel(str(yLabel), fontsize=20)
    plt.xlabel('TIMESTAMP (%d samples)' % xticks, fontsize=20)
    # print the legand box (with color-coded operations)
    leg=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=19)
    plt.subplots_adjust(left=0.12,bottom=0.18, right=0.9, top=0.85, wspace=0.2,hspace=0.2)
# use the filename as the plot title
    plt.suptitle('%s '% theFile, fontsize=24)
# save the PDF - name convention is jobID_stagename.PDF
    basenm=os.path.basename(theFile)
# strips off the final "/" if its there
    pathnm=os.path.dirname(theFile)
# grab the tail of the path and prepend it to the PDF fname       
    prepend=os.path.basename(pathnm)
    fname=prepend+'_'+basenm.split('.')[0]+'_'+plotType.upper()+'.pdf'
    plt.savefig(fname, format='pdf', dpi=1000)
    print('> Created PDF chart: '+fname)
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
        label1 = "Avg-ResTime"
        label2 = "Avg-ProcTime"
        units = " (ms)"
    elif args.type == 'throughput':
# set up for plotting Throughput
        plot = "throughput"
        label1 = "Throughput"
        label2 = "Bandwidth"
        units = " (ops)"
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
            plot_stats(file, plot, label1, label2, units)
        else:
            print "Skipping CSV file: ", file

# Wait for user input
#        os.system('read -s -n 1 -p "Press any key to continue..."')
#        print

# END
