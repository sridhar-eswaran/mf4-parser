# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 11:33:00 2021

@author: SESWARAN
"""
from asammdf import MDF
import pandas as pd
import numpy as np
from pathlib import Path

class mdfSubset:  
        """        
        Parameters
        ----------
        subsetDataAslist : List
            List of ASAM Signal objects
        mdfname : string
            name for the new object
        Returns
        -------
        TYPE
            returns a object with signallist and filename

        """
        def __init__(self,subsetDataAslist,mdfname): 
            if isinstance(subsetDataAslist,list):
                    self.subsetList = subsetDataAslist 
                    self.name = mdfname 
            else:
                print('Incorrect object datatype')
        
        def createSubset(filepath_MF4,filepath_signalListCsv):
            """        
            Parameters
            ----------
            filepath_MF4 : windowsPath / string
                either windowsPath or a string of full windows path of the file
            filepath_signalListCsv : csv
                Must contain Columns [Name,Type,Signal]
                Name: Display name of a signal
                Type: 'Cont' or 'State' 
                    e.g. speed/ accel -> continous | status(on/off) -> state based (enums)
            Returns
            -------
            TYPE
                returns a list with signals extracted (listed in csv) from mf4 and filename
            """
            filename = Path(filepath_MF4).name
            mf4data = MDF(filepath_MF4)
            signalCsv = pd.read_csv(filepath_signalListCsv)
            subsetList = []
            noSigMissing = 0
            for signals in range(20): #len(signalCsv iterate for all signal in the CSV
                try:                      
                    sg_pos=mf4data.whereis(signalCsv.Signal[signals])            
                    for k in range(len(sg_pos)): # valid group and channel selection
                        gr_nr = sg_pos[k][0] # k is the list index of available channel groups
                        ch_nr = sg_pos[k][1] 
                        sdata = mf4data.get(None,gr_nr,ch_nr) # find the signal 
                      
                    sdata.Type=signalCsv.Type[signals] 
                    sdata.display_name = signalCsv.Name[signals]
                    subsetList.append(sdata)           
                except:     # signal not found in the measurement file 
                    noSigMissing +=1
                    print(f'{noSigMissing}. {signalCsv.Name[signals]} not found')                        
            return mdfSubset(subsetList,filename)
    
    
        def mdfConcat(mdfObjSubsetBase,mdfObjSubsetIncoming,newMdfname):
            """
            mdfConcat(mdfObjSubsetBase,mdfObjSubsetIncoming,newMdfname)
            Signal names and index should match in both the files

            Parameters
            ----------
            mdfObjSubsetBase : mdfSubsetObject
                source module: subset created using createSubset method
            mdfObjSubsetIncoming : mdfSubsetObject
                append module: subset created using createSubset method
            newMdfname : string
                new name for the concatinated module.

            Returns
            -------
            TYPE
                mdfSubsetObject -> mdfObjSubsetBase + mdfObjSubsetIncoming

            """
            dataBase = mdfObjSubsetBase.subsetList
            dataIn = mdfObjSubsetIncoming.subsetList
            subsetListMerged = []
            for signals in range(len(dataBase)):
                if dataBase[signals].name == dataIn[signals].name:
                    mergeSig = dataBase[signals].extend(dataIn[signals])
                    subsetListMerged.append(mergeSig)
                else:
                   print(f'Signal index mismatch \n Index = {signals} baseSignal = dataBase[signals].name IncomingSignal = dataAppend[signals].name')
            return mdfSubset(subsetListMerged,newMdfname)
               
        def getTimestamps(self):
            sample = self.subsetList[0]
            return [sample.timestamps[0],sample.timestamps[-1]]
        
        def getSignalNames(self):
            data = self.subsetList
            names = []
            for signals in range(len(data)):
                names.append(data[signals].name)
            return names
                
        
        def getSamplesize(self,signalName):
            data = self.subsetList
            samples = 0        
            for signals in range(len(data)):
                if data[signals].name == signalName:
                    samples = len(data[signals])            
            if samples == 0:
                print('Signal Not found')
            return samples
        
        def mdfResample(self,timestep):
            data = self.subsetList
            fname = self.name
            ref  = data[0] # first signal in the list chosen as reference for timestamps
            start = float("{:.3f}".format(ref.timestamps[0])) # get the start time and reduce decimal places to 3
            end = float("{:.3f}".format(ref.timestamps[-1])) # get the last time and reduce decimal places to 3
            timesteps = np.linspace(start,end,round((end - start)/timestep))
            subsetListResampled = []
            # resample signals
            for signals in range(len(data)):
                if data[signals].Type == 'State': # state output signals like status signals
                        resampled = data[signals].interp(timesteps)
                        subsetListResampled.append(resampled)
                elif data[signals].Type == 'Cont': # continous signals physical mesurement signals
                        resampled = data[signals].interp(timesteps,interpolation_mode = '1') 
                        subsetListResampled.append(resampled)
            return mdfSubset(subsetListResampled,fname)
        
        def createDataSeries(self): 
            data = self.subsetList 
            dataSeries = []
            for signals in range(len(data)):
                samples = data[signals].samples   
                timestamps = data[signals].timestamps
                series = pd.Series(samples,timestamps,name = data[signals].display_name)
                if isinstance(samples[0],bytes): #convert data type for enumarated values like ACCStatus, TSRSpdLimit
                    values=[]    
                    for timestep in range(len(samples)):
                        values.append(samples[timestep].decode("utf-8"))                    
                    series = pd.Series(values,timestamps,name = data[signals].display_name)
                    dataSeries.append(series)                
                else: # signals does not require conversion, non-byte data types like A1,A2,etc
                    dataSeries.append(series) 
            return dataSeries
        
        def createDataTable(self,timesteps):
            resample = self.mdfResample(timesteps)
            dataSeries = resample.createDataSeries()
            dataTable = pd.DataFrame()
            for signals in range(len(dataSeries)):
                dataTable[dataSeries[signals].name] = dataSeries[signals].values
            dataTable.index = dataSeries[0].index
            return dataTable
                
        def exportCSV(self,timesteps,outputFilename):
            """
            exportCSV(timesteps,'outputFilename.csv')
            
            Parameters
            ----------
            timesteps : float/int
                >0 to <2
            outputFilename : string include .csv
                file name for output CSV

            Returns
            -------
            None.

            """
            datatable = self.createDataTable(timesteps)
            datatable.to_csv(outputFilename,index_label='timestamps')

    
    