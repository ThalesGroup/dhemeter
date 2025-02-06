# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import os
import json
import time
import argparse
import datetime
import calendar
import subprocess

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'TEMPORAL INTERPOLATION'
    execution_dict['execution_status'] = 0 #request started
    execution_dict['attempts'] = 0 
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict

def format_hour(first_forecast):
    # first_forecast is a string with the format YYYY-MM-DDTHH:MM:SSZ
    # format the string to a datetime object with the format YYYY-MM-DD,HH:MM:SS
    date = datetime.datetime.strptime(first_forecast, '%Y-%m-%dT%H:%M:%S.%fZ')
    # then, format the date to a string with the format YYYY-MM-DD,HH:MM:SS
    # format the date to YYYY-MM-DD,HH:MM:SS
    date = date.strftime('%Y-%m-%d,%H:%M:%S')
    return date

def infos(file_name):
    infos_command = 'cdo -info ' + output_dir + '/' + file_name
    ncdump_command = 'ncdump -h ' + output_dir + '/' + file_name
    return infos_command, ncdump_command

def main(output_dir, execution_file, input_dir, params_time):
    Logs = Exec_Logs()
    # start execution time
    start_time = time.time()

    # from the parameters, get the first interpolation hour
    with open(params_time, 'r') as f:
        params_time = json.load(f)
        run_time = params_time['run_time']
        forecasts = params_time['forecasts']
        first_forecast = forecasts[0]

    # format the first_hour
    first_hour = format_hour(first_forecast)

    attempts = 0
    successfull_attempts = 0
    file_list = []

    # try to remap the file with the target grid
    for file in os.listdir(input_dir):
        attempts += 1
        try:
            file_interp = file[:-3] + '_interp.nc'
            remap_command = 'cdo -inttime,' + first_hour + ',1hour ' + input_dir + '/' + file + ' ' + output_dir + '/' + file_interp
            if os.system(remap_command) == 0:
                infos_command, ncdump_command = infos(file_interp)
                if os.system(infos_command + ' && ' + ncdump_command) == 0:
                    successfull_attempts += 1
                    file_list.append(file_interp)
                else:
                    raise Exception('Error in remapping the file')
            else:
                raise Exception('Error in remapping the file')
        except Exception:
            pass

    # end execution time
    end_time = time.time()
    execution_time = end_time - start_time
    Logs['execution_time'] = round(execution_time, 2)
    Logs['attempts'] = attempts
    Logs['successfull_attempts'] = successfull_attempts
    Logs['file_list'] = file_list

    # print the number of successfull attempts over the total number of attempts
    if attempts == 0 and successfull_attempts == 0:
        Logs['execution_status'] = 24 # no files to download
    elif successfull_attempts == 0 and attempts != 0:
        Logs['execution_status'] = 24 # no files downloaded
    elif successfull_attempts != 0 and attempts != 0:
        Logs['execution_status'] = 20 # request finished
    else:
        Logs['execution_status'] = 50 # error in request

    # dump the dict into a json file /execution/logs_IFS.json
    with open(execution_file, 'w') as logs:
        json.dump(Logs, logs, indent=4)


if __name__ == '__main__':
    #try:
        # with argparse, create a parser object
        parser = argparse.ArgumentParser()
        
        # the parameters are : --params_time, --params_variables, --output_dir, --execution_file
        parser.add_argument('--logs_file', type=str, help='Path to the execution file')
        parser.add_argument('--params_time', type=str, help='Path to the time parameters file')
        parser.add_argument('--input_dir', type=str, help='Path to the input directory')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        
        # parse the arguments
        args = parser.parse_args()
        
        # assign the arguments to variables
        params_time = args.params_time
        output_dir = args.output_dir
        input_dir = args.input_dir
        logs_file = args.logs_file

        main(output_dir, logs_file, input_dir, params_time)
'''except:
Logs = Exec_Logs()
Logs['execution_status'] = 50
# dump the dict into a json file /execution/logs_GFS.json
with open(logs_file, 'w') as logs:
    json.dump(Logs, logs, indent=4)'''
