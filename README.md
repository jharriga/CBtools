# CBtools
COSbench result post-processing tools

# cbparser
Generates COSbench General Report from COSbench CSV files
Imports numpy
Requires one argument: -d (directory)

Tested with python 2.7.5
## Sample usage:
* $ ./cbparser.py -d w169-hybrid/

Produces file ...

# cbplot
Generates PNGs from COSbench CSV files
Imports matplotlib
Requires two arguments: -d (directory) and -t (plotType)

NOTE: excludes CSV files ending with "-worker.csv" AND results from 'init' stages, since they are empty

Tested with python 2.7.5
## Sample usage:
* $ ./cbplot.py -d w169-hybrid/ -t throughput
* $ ./cbplot.py -d w161-delete_write -t latency
