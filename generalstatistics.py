# Method to compute the mean and standard deviation of time durations associated
# with black screens (both strict and lenient), shot transitions and silent portions
# of the videos.
# 
# Input: 
#    1. The name of the directory that contains the CSV files for black screens,
#       shot transitions and silent sections of the videos.    
#    2. The name of the log file to which the output is written.
#
# Version : 1.0 
# Last Updated : 03/09/2023 (Vivek Vasudeva)

import pandas as pd
import numpy 
import os

logFile = "D:\\projects\\ad conditioning\\classifications_for_30_videos\\log.csv";

dirName = "D:\\projects\\ad conditioning\\classifications_for_30_videos";

fileList = os.listdir(dirName);

for f in fileList:
    
    # check if file name contains the text "black_screen" or "shot_transition"
    # or "silence".
    
    nFound1 = f.find("black_screen");
    nFound2 = f.find("shot_transition");
    nFound3 = f.find("silence");

    if ((nFound1 >= 0) | (nFound2 >= 0) | (nFound3 >= 0)) :
    
        # If the file name contains any of the specific strings, then
        # obtain the relevant statistics.
        
        # get the full name of the file
        fileNameCur = dirName + "\\" + f;
        
        dataCur = pd.read_csv (fileNameCur);
        
        dfCur = pd.DataFrame(dataCur);
    
        # get the indicator values
        indicatorValues =  dfCur.iloc[:,2];
    
        beginTimes = dfCur.iloc[:,0];
        endTimes = dfCur.iloc[:,1];
    
        # get the time durations corresponding to a black screen, or shot
        # transition or silence.
        
        durationList = [];
        
        i = 0;
            
        while i < len(dfCur):
        
            if (indicatorValues[i] == 1):
                            
                durationCur = endTimes[i] - beginTimes[i];
                
                durationList.append(durationCur);
                 
            #endif
            
            i = i + 1;
        
        #end while
    
        # get the size of durationList
        sizeCur = len(durationList);
    
        # get the average value of the signal
        meanCur = numpy.mean(durationList);
    
        # get the standard deviation of the signal
        stDevCur = numpy.std(durationList);
        
    
        # output the statistics to the log file
        logMessage = ""
        
        logMessage = logMessage + f + "," + "noOfValues," + str(sizeCur) + "\n";
        logMessage = logMessage + f + "," + "mean," + str(meanCur) + "\n";
        logMessage = logMessage + f + "," + "stDev," + str(stDevCur) + "\n";
         
        # output the log message
        pFile = open(logFile, "a");
        pFile.write(logMessage);  
        pFile.close();     
    
    #end if

#end for
    
    
    
    
    