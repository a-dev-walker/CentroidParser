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
import time


#Function for getting the distances between points based off the df input
def determine_neighbours(function_df):

    for column in function_df:
        if function_df[column].dtype == 'float64':
          function_df[column]=pd.to_numeric(function_df[column], downcast='float')

    

    #Getting the centroid positions of all the positive cells
    posX = function_df['Centroid X µm'].values
    posY = function_df['Centroid Y µm'].values

    #Finding the distances between centroids
    coords = np.vstack((posX,posY)).T

    output_small_dtype = np.empty((coords.shape[0],1),dtype=np.float64)

    dist_sums = np.empty((1,coords.shape[0])).T
    for q in range(coords.shape[0]):
        output_small_dtype = np.empty((coords.shape[0],1),dtype=np.float64)
        y = distance.cdist(coords,[coords[q]],out = output_small_dtype)

        y[y<=0] = np.nan #getting rid of negative and 0 values
        y[y>500] = np.nan #Getting rid of values that are greater than radius 5mm

        dist_sums[q] = np.sum(~np.isnan(y[:]))

    # mostCrowded = np.argmax(dist_sums)
    # hotSpotX = df.iloc[mostCrowded,0]
    # hotSpotY = df.iloc[mostCrowded,1]
    # print(f'{function_type} hotspot is at point: ',hotSpotX,',',hotSpotY)

    return dist_sums



def Main():

    ##print time to let user know how long processes are taking
    print(time.localtime())

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
    circleRadius = args.Radius_of_hotspot_in_mm ##This is never used lol

    #Inputting the data from the csv 
    fileName = wd + '\\' + inputFileName
    starting_df = pd.read_csv(fileName,sep = '\t', usecols=[2,5,6])
    print(pd.DataFrame.head(starting_df,5))
    #starting_df = starting_df.set_index("Class")

    #Cutting data into fourth's to run faster and use less memory
    split = True
    if(split):
        starting_df = starting_df.iloc[::4]


    #Adding all cell-cell distances to starting_df and making it all_cell_df
    all_cell_df = pd.DataFrame.copy(starting_df)
    all_cell_distances = determine_neighbours(starting_df)
    all_cell_df['Neighbor_counts'] = all_cell_distances.tolist()

    #Creating positive cell only df and getting distances for that as well
    pos_cell_df = starting_df.drop(starting_df.index[starting_df['Class'] == 'Negative'])
    positive_cell_distances = determine_neighbours(pos_cell_df)
    pos_cell_df['Neighbor_counts'] = positive_cell_distances.tolist()


    #Getting rid of negative cells from all_cell_df to allow for comparison
    all_cell_df_without_negative = all_cell_df.drop(all_cell_df.index[all_cell_df['Class'] == 'Negative'])


    #converting pandas lists to floats to allow for mathematic operations
    all_cell_df_without_negative['Neighbor_counts'] = all_cell_df_without_negative['Neighbor_counts'].map(lambda x: float(x[0]))
    pos_cell_df['Neighbor_counts'] = pos_cell_df['Neighbor_counts'].map(lambda x: float(x[0]))

    #Comparing datasets to get percentage score
    positivity_percentages = pos_cell_df['Neighbor_counts'] / all_cell_df_without_negative['Neighbor_counts']
    max_positivity = pd.Series.argmax(positivity_percentages)

    hotSpotX = all_cell_df_without_negative.iloc[max_positivity,1]
    hotSpotY = all_cell_df_without_negative.iloc[max_positivity,2]

    print('Hotspot is at point: ',hotSpotX,',',hotSpotY)


    #Logging data for later use
    log.write('HotSpot for '+ inputFileName+' is at point: '+ str(hotSpotX)+','+str(hotSpotY)+'\n')
    log.close()



if __name__ == "__main__":
    Main()
