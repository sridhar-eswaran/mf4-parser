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
	
## Examples

`

	#Create a subset from a larger MF4 file
	from mf4parser import mdfSubset as ms
	#select mf4 file
	mf4_file1 = r'C:\users\sridhar\files\measurementFile01.MF4'
	mf4_file2 = r'C:\users\sridhar\files\measurementFile02.MF4'
	#select the signal list (csv) file containg list of signals to be extracted (sample can be found in repo)
	signalList = r'C:\users\sridhar\files\signalList.csv'
	# create a subset
	subset1 = ms.createSubset(mf4_file1,signalList)
`

	#to get the info of a subset
	subset1.getTimestamps()
`
	OUTPUT:
	[0.060000000, 299.900000000]
`

	subset1.getSignalNames()
`
	OUTPUT:
	['Vx',
	'Vy',
	'Ax',
	'Ay']
`

	subset1.getSamplesize('Ax')
`
	OUTPUT:
	2500
`

	#create another subset
	subset2 = ms.createSubset(mf4_file2,signalList)
	## to get the info of a subset
	subset2.getTimestamps()
`
	OUTPUT:
	[299.910000000, 600.100000000]
`

	subset2.getSignalNames()
`
	OUTPUT:
	['Vx',
	'Vy',
	'Ax',
	'Ay']
`

	subset2.getSamplesize('Ax')
`
	OUTPUT:
	2508
`

	# concatinate subset files
	subset12 = ms.mdfConcat(subset1,subset2,'newSubsetname')
`

	## Concatinated subset info
	subset12.getTimestamps()
`
	OUTPUT:
	[0.060000000, 600.100000000]
`

	subset12.getSignalNames()
`
	OUTPUT:
	['Vx',
	'Vy',
	'Ax',
	'Ay']
`

	subset12.getSamplesize('Ax')
`
	OUTPUT:
	5008
`

	# create data series from a subset (creates a pandas series of signals (TimeStamps Vs SampleValue)
	dataseries = subset12.createDataSeries()
	
	# Create data table from a subset (creates a pandas data frame (Timestamps | signal1 | signal2 | signal3))
	timestep_to_resample = 0.02 # 20milliseconds
	dataTable = subset12.createDataTable(timestep_to_resample) 
	
	# export subset to a csv
	subset12.exportCSV(timestep_to_resample,'csvFile.csv')
	
	
	