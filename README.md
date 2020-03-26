# CBtools
COSbench result post-processing tools

# CBreport
Generates COSbench General Report from COSbench CSV files
Imports numpy
Requires one argument: -d (directory)

Tested with python 2.7.5
## Sample usage:
* $ ./CBreport.py -d archive/w21-hybridSS

Produces file ...

# CBplot
Generates PNGs from COSbench CSV files
Imports matplotlib
Requires two arguments: -d (directory) and -t (plotType)

NOTE: excludes CSV files ending with "-worker.csv" AND results from 'init' stages, since they are empty

Tested with python 2.7.5
## Sample usage:
* $ ./CBplot.py -d archive/w21-hybridSS -t throughput
* $ ./CBplot.py -d archive/w21-hybridSS -t latency
