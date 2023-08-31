# Method to identify files that contain either frame-based or window-based 
# place transition signal values that are more than 3 standard deviations 
# from the mean.
# 
# Input: 
#    1. The name of the directory that contains the CSV files for place 
#       transitions.
#    2. The name of the log file to which the output is written.
#
# Version : 1.0 
# Last Updated : 03/09/2023 (Vivek Vasudeva)

import pandas as pd
import numpy 
import os

MAX_NO_OF_STANDARD_DEVIATIONS_ALLOWED = 3

logFile = "D:\\projects\\ad conditioning\\classifications_for_30_videos\\log.csv";

dirName = "D:\\projects\\ad conditioning\\classifications_for_30_videos";

fileList = os.listdir(dirName);

for f in fileList:
    
    # check if file name contains the text "black_screen" or "shot_transition"
    # or "silence".
    
    nFound1 = f.find("place_transitions");

    if (nFound1 >= 0):
    
        # get the full name of the file
        fileNameCur = dirName + "\\" + f;
        
        dataCur = pd.read_csv (fileNameCur);

        dfCur = pd.DataFrame(dataCur);
         
        # get the signal values for frame-based place transitions.
        signalListPlaceTransitionFrame = dfCur["place_transition_frame_to_frame"];
        
        # get the average value of the signal
        meanPlaceTransitionFrame = numpy.mean(signalListPlaceTransitionFrame);
    
        # get the standard deviation of the signal
        stDevPlaceTransitionFrame = numpy.std(signalListPlaceTransitionFrame);
        
        # set the limits.
        curLimitMin = meanPlaceTransitionFrame - MAX_NO_OF_STANDARD_DEVIATIONS_ALLOWED * stDevPlaceTransitionFrame;
                      
        curLimitMax = meanPlaceTransitionFrame + MAX_NO_OF_STANDARD_DEVIATIONS_ALLOWED * stDevPlaceTransitionFrame;
    
        noOfViolationsPlaceTransitionsFrame = 0;
        
        i = 0;
            
        while i < len(dfCur):
        
            if ((signalListPlaceTransitionFrame[i] <= curLimitMin) 
                    | (signalListPlaceTransitionFrame[i] >= curLimitMax)):
                            
                noOfViolationsPlaceTransitionsFrame = noOfViolationsPlaceTransitionsFrame + 1;
                 
            #endif
            
            i = i + 1;
        
        #end while
    
    
        # get the signal values for window-based place transitions.
    
        signalListPlaceTransitionWindow = dfCur["place_transition_window_to_window"];
        
        # get the average value of the signal
        meanPlaceTransitionWindow = numpy.mean(signalListPlaceTransitionWindow);
    
        # get the standard deviation of the signal
        stDevPlaceTransitionWindow = numpy.std(signalListPlaceTransitionWindow);
        
        # set the limits.
        curLimitMin = meanPlaceTransitionWindow - MAX_NO_OF_STANDARD_DEVIATIONS_ALLOWED * stDevPlaceTransitionWindow;
                      
        curLimitMax = meanPlaceTransitionWindow + MAX_NO_OF_STANDARD_DEVIATIONS_ALLOWED * stDevPlaceTransitionWindow;
    
        
        noOfViolationsPlaceTransitionsWindows = 0;
        
        i = 0;
            
        while i < len(dfCur):
        
            if ((signalListPlaceTransitionWindow[i] <= curLimitMin) 
                    | (signalListPlaceTransitionWindow[i] >= curLimitMax)):
                            
                noOfViolationsPlaceTransitionsWindows = noOfViolationsPlaceTransitionsWindows + 1;
                 
            #endif
            
            i = i + 1;
        
        #end while
    
        
        # output the number of violations
        
        logMessage = ""
        
        logMessage = logMessage + f + "," + "noOfViolationsPlaceTransitionsFrame," + str(noOfViolationsPlaceTransitionsFrame) + "\n";
        logMessage = logMessage + f + "," + "noOfViolationsPlaceTransitionsWindows," + str(noOfViolationsPlaceTransitionsWindows) + "\n";
         
        # output the log message
        pFile = open(logFile, "a");
        pFile.write(logMessage);  
        pFile.close();     
    
    # end if
    
#end for
    
    
    
    
    