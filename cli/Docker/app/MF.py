# function to find the nearest Radio Sondage WMO code to a given lat/lon from a list of WMO codes
# the list of WMO codes is read from a csv file in ./Stations/RS_MF.csv

import pandas as pd
import numpy as np
import math
import os

def find_nearest(lat,lon):
    # read in the list of ICAO codes
    df = pd.read_csv('Stations/RS_MF.csv')
    # calculate the distance between the given lat/lon and each ICAO code
    df['distance'] = df.apply(lambda row: math.sqrt((row['LAT']-lat)**2+(row['LON']-lon)**2), axis=1)
    # find the minimum distance rounded to 3 decimal places
    min_distance = df['distance'].min()
    # find the line in the dataframe with the minimum distance
    nearest_RS = df.loc[df['distance'] == min_distance]['ID'].values[0]
    # RS id is supposed to be a an integer of 5 digits but some are 4 digits so we need to add a 0 at the beginning
    if len(str(nearest_RS)) < 5:
        for i in range(5-len(str(nearest_RS))):
            nearest_RS = '0'+str(nearest_RS)
    location = df.loc[df['distance'] == min_distance]['LOCATION'].values[0]
    # lat/lon of the nearest ICAO code
    nearest_lat = df.loc[df['distance'] == min_distance]['LAT'].values[0]
    nearest_lon = df.loc[df['distance'] == min_distance]['LON'].values[0]
    print('RadioSonde identifier code found: ', nearest_RS, location, nearest_lat, nearest_lon)
    return nearest_RS, location, nearest_lat, nearest_lon


def find_RS_Station(ID):
    # create a function to try and find the IGRA id code in the list of IGRA id codes
    # read in the list of IGRA codes
    # try cast ID to int
    cwd = os.getcwd()
    try:
        ID = int(ID)
    except:
        return False
    df = pd.read_csv('Stations/RS_MF.csv')
    # try to find the line in the dataframe with the WMO code
    try :
        station_name = df.loc[df['ID'] == ID]['LOCATION'].values[0]
        lat = df.loc[df['ID'] == ID]['LAT'].values[0]
        lon = df.loc[df['ID'] == ID]['LON'].values[0]
        print('RadioSonde identifier code found: ', ID, station_name, lat, lon)
        return True
    except:
        return False
