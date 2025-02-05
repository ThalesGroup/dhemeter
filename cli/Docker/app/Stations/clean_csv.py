# function to clean the csv file containing the list of stations and their ICAO codes 
# the list of ICAO codes is read from a csv file in ./Stations/isd_Station_Name.csv
# if the ICAO code is not in the list of stations, it is removed from the list

import pandas as pd
import numpy as np
import math

def clean_csv_names():
    # read in the list of ICAO codes and station names
    # ICAO codes are in the column 'ICAO'
    df = pd.read_csv('./Stations/isd_Station_Name.csv')
    # read which ICAO Codes are empty
    # empty ICAO codes are given as 'NaN' in the csv file
    # find the lines in the dataframe with empty ICAO codes
    empty_ICAO = df.loc[df['ICAO'].isnull()]
    print(empty_ICAO.index)
    # delete the lines with empty_ICAO indexes from the dataframe
    df = df.drop(empty_ICAO.index)
    # reset the index
    df = df.reset_index(drop=True)
    # save the dataframe to a csv file
    df.to_csv('./Stations/isd_Station_Name.csv',index=False)
    return df
def clean_csv_loc():
    df = pd.read_csv('./Stations/isd_Station_Name.csv')
    # read which lat and lon values are empty at the same time
    # empty lat and lon values are given as '0.0' in the csv file
    # find the lines in the dataframe with empty lat and lon values
    empty_lat = df.loc[df['LAT'] == 0.0]
    empty_lon = df.loc[df['LON'] == 0.0]
    # count the number of lines with empty lat and lon values
    print(len(empty_lat.index))
    print(len(empty_lon.index))
    # find the intersection of the two sets of indexes
    empty_lat_lon = empty_lat.index.intersection(empty_lon.index)
    # print the intersection
    print(empty_lat_lon)
    # print the ICAO codes of the stations with empty lat and lon values
    print(df.loc[empty_lat_lon,'ICAO'])
    empty_ICAO = df.loc[empty_lat_lon,'ICAO']
    
    # delete the lines with empty ICAO codes from the dataframe
    df = df.drop(empty_lat_lon)
    # reset the index
    df = df.reset_index(drop=True)
    # save the dataframe to a csv file
    df.to_csv('./Stations/isd_Station_Name2.csv',index=False)
    return df
    
import pandas as pd
import numpy as np
import os
import argparse


# create a function to suppress all the stations that are not active anymore
def suppress_inactive_stations():
    # open the IGRA2.csv file
    df = pd.read_csv("IGRA2_raw.csv")
    # print the dataframe
    print(df)
    # if END == 2023 then the station is still active
    # add a column ACTIVE to the dataframe
    df["ACTIVE"] = np.where(df["END"] == 2023, "True", "False")
    # create a new dataframe with only the active stations
    df_active = df[df["ACTIVE"] == "True"]
    # save the dataframe in a new csv file
    df_active.to_csv("IGRA.csv", index=False)


# test the function
#clean_csv_loc()
