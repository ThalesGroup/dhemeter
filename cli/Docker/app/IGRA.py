# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
# function to find the nearest IGRA code to a given lat/lon from a list of IGRA codes
# the list of IGRA codes is read from a csv file in ./Stations/IGRA.csv

import pandas as pd
import numpy as np
import math
import os



def find_nearest(lat,lon):
    cwd = os.getcwd()
    # read in the list of ICAO codes
    df = pd.read_csv('Stations/IGRA.csv')
    # calculate the distance between the given lat/lon and each ICAO code
    df['distance'] = df.apply(lambda row: math.sqrt((row['LAT']-lat)**2+(row['LON']-lon)**2), axis=1)
    # find the minimum distance rounded to 3 decimal places
    min_distance = df['distance'].min()
    # find the line in the dataframe with the minimum distance
    nearest_IGRA = df.loc[df['distance'] == min_distance]['ID'].values[0]
    location = df.loc[df['distance'] == min_distance]['LOCATION'].values[0]
    # lat/lon of the nearest ICAO code
    nearest_lat = df.loc[df['distance'] == min_distance]['LAT'].values[0]
    nearest_lon = df.loc[df['distance'] == min_distance]['LON'].values[0]
    print('IGRA identifier code found: ', nearest_IGRA, location, nearest_lat, nearest_lon)
    return nearest_IGRA, location, nearest_lat, nearest_lon


def find_IGRA(ID):
    cwd = os.getcwd()
    # create a function to try and find the IGRA id code in the list of IGRA id codes
    # read in the list of IGRA codes
    df = pd.read_csv('Stations/IGRA.csv')
    # try to find the line in the dataframe with the IGRA code
    try :
        station_name = df.loc[df['ID'] == ID]['LOCATION'].values[0]
        lat = df.loc[df['ID'] == ID]['LAT'].values[0]
        lon = df.loc[df['ID'] == ID]['LON'].values[0]
        print('IGRA identifier code found: ', ID, station_name, lat, lon)
        return True
    except:
        return False
