# mf4-parser
To extract set of signals from a MDF4 (mf4) files

## Features
	* Create __mdfSubset__ in two ways
		* Instantiate with a list of 'asammdf.Signals'
		* Create a new subset from a larger MDF(.mf4) file with a list of signals in csv 
	* Concatinate two mdfSubsets to create a new file (joins the each signals)
	* Get timestamps (start,end) of a mdfSubset object
	* Get the name of the signals in the mdfSubset
	* Get the sample size of a signal in the mdfSubset
	* Resample the signals in the mdfSubset to a different timestep
	* Create a list of pandas-series objects (timestamps,samples) with the signals in the mdfSubset
	* Create a data table with signals in the mdfSubset
	* Export signals in the mdfSubset to a csv file 

## Requirements
	- Python >=3.7
	
## Installation

### pip 
	pip install mf4parser
	
### git 
	clone the repo [mf4parser](https://github.com/sridhar-eswaran/mf4-parser.git)