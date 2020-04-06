# CBtools
COSbench result post-processing tools  
Tested with python 2.7.5

# CBreport
Generates COSbench General Report from COSbench results   
Requires one argument: -d (directory)  
USAGE: $ ./CBreport.py --help  
NOTE: Requires numpy (# pip install numpy)  

## Sample usage:
* $ ./CBreport.py -d archive/w21-hybridSS

Produces file "w21-hybridSS-CBreport.txt"

# CBplot
Generates PNGs from COSbench CSV files  
Requires two arguments: -d (directory) and -t (plotType)  
Optional arg: -n (MaxSamples)  <-- Default value: 5000  
USAGE: $ ./CBplot.py --help  
NOTE: Requires matplotlib (# pip install matplotlib)  

## Sample usage:
* $ ./CBplot.py -d archive/w21-hybridSS -t throughput
* $ ./CBplot.py -d archive/w21-hybridSS -t latency
