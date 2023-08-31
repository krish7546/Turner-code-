# Method to identify files for which the black screen responses are either more
# than 3 seconds long or are within 2 minutes of each other.
# 
# Input: 
#    1. The name of the directory that contains the CSV files for black screens.
#    2. The name of the log file to which the output is written.
#
# Version : 1.0 
# Last Updated : 03/09/2023 (Vivek Vasudeva)

import pandas as pd
import os

dirName = "D:\\projects\\ad conditioning\\classifications_for_30_videos";

logFile = "D:\\projects\\ad conditioning\\classifications_for_30_videos\\log.csv";

MAX_BLACK_SCREEN_DURATION = 0.5

MAX_TIME_INTERVAL_BETWEEN_TWO_BLACK_SCREENS = 120

fileList = os.listdir(dirName);

for f in fileList:
    
    # check if file name contains the text "black_screen".
    
    nFound = f.find("black_screen");

    if (nFound >= 0):

        # If the file name contains any of the specific strings, then
        # obtain the relevant statistics.
        
        # get the full name of the file
        fileNameCur = dirName + "\\" + f;
        
        dataCur = pd.read_csv (fileNameCur);
        
        dfCur = pd.DataFrame(dataCur);
         
        startTimes = dfCur["start_time"]
        endTimes = dfCur["end_time"]

        # get the indicator values
        indicatorValues = dfCur.iloc[:,2];

        # durationList is the list of time durations for all black screens.       
        
        durationList = []

        # elapseTimeList is the list of time intervals between two successive 
        # black screens.       
        
        elapseTimeList = []
        
        noOfLongBlackScreens = 0;
        noOfCloseBlackScreens = 0;
        
        foundFirstBlackScreen = 0;
        endTimePreviousBlackScreen = 0;
        
        i = 0

        while i < len(dfCur):
        
            curDuration = endTimes[i] - startTimes[i];
            
                   
            # check whether this black screen is a long black screen.

            if ((indicatorValues[i] == 1) & (curDuration >= MAX_BLACK_SCREEN_DURATION)):
                
                noOfLongBlackScreens = noOfLongBlackScreens + 1; 
            
                durationList.append(curDuration);
            
            #end if
            
            # check for close black screens.
    
            if (indicatorValues[i] == 1):
    
                # if the first black screen has been found, then check whether
                # the elapse time between the current and the previous black
                # screen exceeds the user-specified value.
    
                if (foundFirstBlackScreen == 1):
                    
                    curTimeInterval = startTimes[i] - endTimePreviousBlackScreen;
                    
                    elapseTimeList.append(curTimeInterval);
                    
                    if  (curTimeInterval >= MAX_TIME_INTERVAL_BETWEEN_TWO_BLACK_SCREENS):
                    
                        #print("Added ", i, "with time interval value", curTimeInterval);
                        
                        noOfCloseBlackScreens = noOfCloseBlackScreens + 1;
    
                        # update the value of endTimePreviousBlackScreen
                        endTimePreviousBlackScreen = endTimes[i];
    
                    else:
                        
                        # update the value of endTimePreviousBlackScreen
                        endTimePreviousBlackScreen = endTimes[i];
               
                else:       # if (foundFirstBlackScreen == 0):
                    
                    endTimePreviousBlackScreen = endTimes[i];
                    foundFirstBlackScreen = 1;
    
                #endif        
            
            #endif
            
            i = i + 1;
        
        #end while
        
        # output the number of violations
        
        logMessage = ""
        
        logMessage = logMessage + f + "," + "noOfLongBlackScreens," + str(noOfLongBlackScreens) + "\n";
        logMessage = logMessage + f + "," + "noOfCloseBlackScreens," + str(noOfCloseBlackScreens) + "\n";
         
        # output the log message
        pFile = open(logFile, "a");
        pFile.write(logMessage);  
        pFile.close();     
        
    #end if
    
#end for
    
    
    
    
    