# -*- coding: utf-8 -*-
"""
Python Script for processing centroid data for Positive Cell detection
Input takes csv files. Please export detection data from Qupath and convert to csv using excel.
Output gives (x,y) data for positive cell with greatest number of other positive cells within "range"
"""

from scipy.spatial import distance
import argparse
import pandas as pd
import os
import numpy as np

## Creating log files for logging output for later
np.warnings.filterwarnings('ignore')
wd = os.getcwd()
logFileName = wd + '\\logs.txt'
log = open(logFileName, 'a+')

## Creating arguments for commandline usage
parser = argparse.ArgumentParser(description='Processing hotspots and aggregation')
parser.add_argument("cellInformationCSV", type = str)
parser.add_argument("Radius_of_hotspot_in_mm", type = int)
args = parser.parse_args()
inputFileName = args.cellInformationCSV
circleRadius = args.Radius_of_hotspot_in_mm

#Inputting the data from the csv and dropping negative points
fileName = wd + '\\' + inputFileName
df = pd.read_csv(fileName,usecols=[2,5,6])
print(pd.DataFrame.head(df,5))
df = df.set_index("Class")
cellCount = len(df)
df = df.drop("Negative",axis=0)

#Getting the centroid positions of all th epositive cells
posX = df.iloc[:,0].values
posY = df.iloc[:,1].values

#Finding the distances between centroids
coords = np.vstack((posX,posY)).T
distances = distance.cdist(coords,coords)
nanDistances = np.copy(distances)
nanDistances[distances <= 0] = np.nan


##Units are all micrometers
#Picking out the hotspots
hotSpots = np.copy(nanDistances)
hotSpots[nanDistances > 500] = np.nan
test_sum = sum(~np.isnan(hotSpots[:]))
mostCrowded = np.argmax(test_sum)

#reporting hotspots
hotSpotX = df.iloc[mostCrowded,0]
hotSpotY = df.iloc[mostCrowded,1]
print('Hotspot is at point: ',hotSpotX,',',hotSpotY)

#Logging data for later use
log.write('HotSpot for '+ inputFileName+' is at point: '+ str(hotSpotX)+','+str(hotSpotY)+'\n')
log.close()
