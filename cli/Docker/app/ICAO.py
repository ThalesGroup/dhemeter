# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
# function to find the nearest ICAO code to a given lat/lon from a list of ICAO codes
# the list of ICAO codes is read from a csv file in ./Stations/isd_Station_Name.csv

import pandas as pd
import numpy as np
import math

def find_nearest(lat,lon):
    # read in the list of ICAO codes
    df = pd.read_csv('./Stations/isd_Station_Name.csv')
    # calculate the distance between the given lat/lon and each ICAO code
    df['distance'] = df.apply(lambda row: math.sqrt((row['LAT']-lat)**2+(row['LON']-lon)**2), axis=1)
    # find the minimum distance rounded to 3 decimal places
    min_distance = df['distance'].min()
    # find the line in the dataframe with the minimum distance
    nearest_ICAO = df.loc[df['distance'] == min_distance]['ICAO'].values[0]
    station_name = df.loc[df['distance'] == min_distance]['STATION_NAME'].values[0]
    # lat/lon of the nearest ICAO code
    nearest_lat = df.loc[df['distance'] == min_distance]['LAT'].values[0]
    nearest_lon = df.loc[df['distance'] == min_distance]['LON'].values[0]
    print('ICAO code found: ', nearest_ICAO, station_name, nearest_lat, nearest_lon)
    return nearest_ICAO, station_name, nearest_lat, nearest_lon


def find_ICAO(ICAO):
    # create a function to try and find the ICAO code in the list of ICAO codes
    # read in the list of ICAO codes
    df = pd.read_csv('./Stations/isd_Station_Name.csv')
    # try to find the line in the dataframe with the ICAO code
    try :
        station_name = df.loc[df['ICAO'] == ICAO]['STATION_NAME'].values[0]
        lat = df.loc[df['ICAO'] == ICAO]['LAT'].values[0]
        lon = df.loc[df['ICAO'] == ICAO]['LON'].values[0]
        print('ICAO code found: ', ICAO, station_name, lat, lon)
        return True
    except:
        return False
