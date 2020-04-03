#!/usr/bin/python
import numpy as np
import re
import argparse
import collections

# GLOBALS ##############
path=""
optType,opListIndex=[],[]
history="run-history.csv"
workload="workloads.csv"


# BEGIN FUNCTIONS ##################
def bytes_2(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1000.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 2
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + ' ' + unit


def printBasicInfo(out,workloadName):
	print "\nBASIC INFO\n"
	out.write("\nBASIC INFO\n")
	id=workloadName.split("-")[0]
	name=workloadName.split("-")[1]
	hist=path+history
	jobStart = jobEnd = None
	fd=open(hist,"r")
 	for line in fd:
		val=line .split(",")
		if (val[0]==id):
			state=val[len(val)-1].split("@")[0]
			jobEnd=val[len(val)-1].split("@")[1]
			break
	out.write("ID: "+str(id)+"\tName: "+str(name)+"\tState: "+str(state)+"\n")
	print "ID: "+str(id)+"\tName: "+str(name)+"\tState: "+str(state)

	fd.close()
	fName=path+str("/")+workloadName+str("/")+workloadName+str(".csv")
	fd=open(fName,"r")
	fd.next() # Skip Header Line 
	for line in fd:
		val = line.split(",")
		size = len(val)
		if not jobStart:
			jobStart = val[18]. split("@")[1]

	print "Submitted At:"+jobStart+ "  Started At: " +jobStart+ "  Stopped At: "+ jobEnd
	out.write("Submitted At:"+jobStart+ "  Started At: " +jobStart+ "  Stopped At: "+ jobEnd+"\n")
	fd.close()

def printFinalReport(out,workloadName):
	fName=path+workload
	fd=open(fName,"r")
	id=workloadName.split("-")[0]
	workerCount=0
	dict={}
	headers = fd.readline().split(",")
	for line in fd:
		val=line.split(",")
		if (val[0].split("-")[0]==id):
			workerCount=val[4]
			val[3]=bytes_2(val[3])
			val[5]=str(val[5])+" ms"
			val[6]=str(val[6])+" ms"
			val[13]=str(val[13])+" op/s"
			val[14]=bytes_2(val[14])
			val[14]=str(val[14])+"/s"
			dict[val[1]]=val
        fd.close()
	size=len(headers)-1
	data,arr=[],[]
	list=[1,2,3,5,6,13,14,15]
	for i in list:
		arr.append(headers[int(i)])
	data.append(arr)
	for key in dict:
		arr=[]
		for i in list:
			arr.append(dict[key][int(i)])	
		data.append(arr)
	fd.close()
	print "\nGENERAL REPORT\n"
	out.write("\nGENERAL REPORT\n")
	widths = [max(map(len, col)) for col in zip(*data)]
        for row in data:
                print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
                out.write("  ".join((val.ljust(width) for val, width in zip(row, widths))))
                out.write("\n")
	
	data,arr=[],[]
	list=[1,7,8,9,10,11,12]
	for i in list:
		arr.append(headers[int(i)])
	data.append(arr)
	for key in dict:
		arr=[]
		for i in list:
			arr.append(dict[key][int(i)])	
		data.append(arr)
	fd.close()
        out.write("\nRESTIME (RT) DETAILS\n")
        print "\nRESTIME (RT) DETAILS\n"
        widths = [max(map(len, col)) for col in zip(*data)]
        for row in data:
                print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
                out.write("  ".join((val.ljust(width) for val, width in zip(row, widths))))
                out.write("\n")


def printRTInfo(out,workloadName):
	resTime=[]
	rt=path+workloadName+"/"+workloadName+"-rt-histogram.csv"
	latencyVal=[60,80,90,95,99,100]
	fd =open(rt,"r")
	for line in fd:
        	val= line.split(",")
        	for i in range(1,len(val)-1,2):
                	optType.append(val[i])
        	break
	size=len(val)-1
	d = np.empty((size, 0)).tolist()
	va = np.empty((size, 0)).tolist()
	start=1
	dict={}
	for line in fd:
        	val= line.split(",")
        	resTime.append(val[0])
        	for i in range(2,len(val),2):
                	index=(i/2)-1
                	d[index].append(val[i].split("%")[0])
                	va[index].append(val[i-1])
	line=["Op-Type","60%-ResTime","80%-ResTime","90%-ResTime","95%-ResTime","99%-ResTime","100%-ResTime"]
	data=[]
	data.append(line)
	for j in xrange(size/2):
	        line=[str(optType[j])]
	       	if optType[j].split("-")[0] not in dict:
			dict[optType[j].split("-")[0]]=1
		else:
			dict[optType[j].split("-")[0]]+=1
		for i in latencyVal:
	                index= int(closest2(d[j],float(i),va[j]))
	                line.append(str(resTime[index].split("~")[1]))
	        data.append(line)
	out.write("\nRESTIME (RT) DETAILS\n")
	print "\nRESTIME (RT) DETAILS\n"
	widths = [max(map(len, col)) for col in zip(*data)]
	counters=n=0	
	odict = collections.OrderedDict(sorted(dict.items()))
	opListIndex.append(1)
	for k, v in odict.iteritems():
		opListIndex.append(v)
	for i in widths:
		n+=i+len("\t")
	start=end=0
	for each in opListIndex:
		end+=int(each)
		for row in data[start:end]:
			print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
			out.write("  ".join((val.ljust(width) for val, width in zip(row, widths))))
			out.write("\n")
			counters+=1
	
		print '-' * n
		out.write('-'*n)
		out.write("\n")
		start=end
	fd.close()


def closest2(list, Number,list2):
     c=a=0 
     for valor in list:
     	if (float(valor) == float(100) and (str(list2[a]) ==str(1))):
		c=a
     	elif( float(valor) != float(100)):
		if ( float(valor) >= float(Number) ):
			return a
     	a+=1
     return c


def printStageInfo(out,workloadName):
        print "\nSTAGES\n"
        out.write("\nSTAGES\n")
    	
	id=workloadName.split("-")[0]
        name=workloadName.split("-")[1]	
	fName=path+workload
	fd=open(fName,"r")
        fd.readline()
	stageNum={}	
        for line in fd:
                val=line.split(",")
                if (val[0].split("-")[0]==id):
                        workerCount=val[4]
	fd.close()
	fName=path+history
	fd=open(fName,"r")
	for line in fd:
                val=line .split(",")
                if (val[0]==id):
			opCount=val[5].split(" ")
	fd.close()
	fName=path+workloadName+"/"+workloadName+".csv"
	fd=open(fName,"r")
	fd.next()
	names,status=[],[]
	for line in fd:
		val=line.split(",")
		regexp = re.compile("s[0-9]-(.*)$")
		names.append(regexp.findall(val[0])[0])
		stageNum[regexp.findall(val[0])[0]]=1
		status.append(val[16])
	fd.close()
	line=["ID", "Name", "Workers", "Op-Info","State"]
	data,arr=[],[]
        data.append(line)	
	for i in xrange(len(stageNum)):
		counter=i*len(opCount)
		arr.append(str(id)+"-s"+str(i))
		arr.append(names[counter])
		arr.append(workerCount)
		line=""
		for j in opCount:
			line+=j+" "

		arr.append(line)
		arr.append(status[counter])
		data.append(arr)
		arr=[]	

        widths = [max(map(len, col)) for col in zip(*data)]
        for row in data:
                print "  ".join((val.ljust(width) for val, width in zip(row, widths)))
                out.write("  ".join((val.ljust(width) for val, width in zip(row, widths))))
                out.write("\n")
# END FUNCTIONS ##################


# MAIN ###################
if __name__ == "__main__":
      	parser = argparse.ArgumentParser(description='Generate COSbench Report')
        parser.add_argument('-d','--archive', help='required: Archive Directory for CosBench Workload Result', required=True)
        arguments = vars(parser.parse_args())
	param=arguments['archive']
	var = param.split('/')
	workloadName = var.pop()
	if not (workloadName):
		workloadName = var.pop()
	path= ""
	for i in var:
		path +=str(i)+"/"
	# FD for output file
	output=workloadName+"-CBreport.txt"
	out=open(output,"w")
	
	# Print Tables
	printBasicInfo(out,workloadName)
	printFinalReport(out,workloadName)
##	printStageInfo(out,workloadName)
##	printRTInfo(out,workloadName)

        print "\nWrote report to: %s" %(output)
out.close()

