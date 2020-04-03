# CBtools
COSbench result post-processing tools  

# CBreport
Generates COSbench General Report from COSbench CSV files  
Requires one argument: -d (directory)  
USAGE: $ ./CBreport.py --help  
NOTE: Requires numpy (# pip install numpy)  

Tested with python 2.7.5
## Sample usage:
* $ ./CBreport.py -d archive/w21-hybridSS

Produces file ...

# CBplot
Generates PNGs from COSbench CSV files  
Requires two arguments: -d (directory) and -t (plotType)  
Optional arg: -n (MaxSamples)
USAGE: $ ./CBplot.py --help  
NOTE: Requires matplotlib (# pip install matplotlib)  

Tested with python 2.7.5
## Sample usage:
* $ ./CBplot.py -d archive/w21-hybridSS -t throughput
* $ ./CBplot.py -d archive/w21-hybridSS -t latency
