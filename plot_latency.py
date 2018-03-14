#!/usr/bin/python
import sys
import datetime as dt
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#from matplotlib.dates import bytespdate2num
import matplotlib.dates as md
import os
import glob

def plot_latency(theFile):
# time, write-ResTime, delete-ResTime
    time, wrt, drt = [],[],[]
    ts_created = os.stat(theFile).st_ctime
    dt_created = dt.datetime.fromtimestamp(ts_created)
    print "PROCESSING:"
    print "> Reading data from: {}".format(theFile)
    print "> File creation time: ", str(dt_created)
#    print "> Date is: ", dt_created.day, dt_created.month, dt_created.year 
    with open(theFile,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        next(plots, None)   # skip first row
        next(plots, None)   # skip second row
        incr = int(0)           # increments timestamp on 24hr period
        cntr = int(0)           # loop counter
        for row in plots:
#           date = dt.datetime.strptime(row[0],"%H:%M:%S").strftime('%H:%M:%S')
            cos_ts = dt.datetime.strptime(row[0],"%H:%M:%S")
            this = cos_ts.replace(year=dt_created.year, month=dt_created.month, day=dt_created.day)
#            print(row[0], this)
            if (cntr > 0):               # check for day rollover 
                if (prev > this.hour):
                    incr += 1               # add a day
                    print ">* Adding a day at: ", str(this)
            date = this + dt.timedelta(days=incr) 
#            print(date)
            time.append(date)
            wrt.append(float(row[5]))	
            drt.append(float(row[6]))
            prev=this.hour
            cntr += 1
    xticks=len(time)
    print "> Number of time values: ", str(xticks)
#   x_data=[]
#   for i in range(xticks):
#	x_data.append(i)	
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

    ax1.plot(time, wrt, color='blue',linewidth=1, marker="o", label='WRITE')
    ax1.plot(time, drt, color='green',linewidth=1, marker="o", label='DELETE')
    plt.tick_params(axis='both', which='major', labelsize=18)
    plt.tick_params(axis='both', which='minor', labelsize=18)
##        plt.xticks(x_data, time, rotation='vertical' )       # save space
    plt.ylabel('LATENCY (ms)', fontsize=20)
    plt.xlabel('TIMESTAMP (%d samples)' % xticks, fontsize=20)
    leg=plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=19)
    plt.subplots_adjust(left=0.12,bottom=0.18, right=0.9, top=0.85, wspace=0.2,hspace=0.2)
    plt.suptitle('LATENCY '+theFile, fontsize=24)
    basenm=os.path.basename(theFile)
    fname=basenm.split('.')[0]+'_latency.pdf'
    plt.savefig(fname, format='pdf', dpi=1000)
    print('> Created PDF chart: '+fname)
#   plt.savefig(sys.argv[2]+'.eps', format='eps', dpi=1000)
#   plt.show()


if __name__ == "__main__":
    for file in list(glob.glob(sys.argv[1]+'/s?-*_failure.csv')):
        plot_latency(file)
# wait for user input
#        os.system('read -s -n 1 -p "Press any key to continue..."')
#        print

# END
