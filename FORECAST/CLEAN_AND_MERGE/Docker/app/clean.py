import os
import json
import xarray
import datetime
import numpy as np
import time
import argparse

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'CLEAN AND MERGE'
    execution_dict['execution_status'] = 0 # request started
    execution_dict['attempts'] = 0
    execution_dict['successfull_attempts'] = 0
    execution_dict['execution_time'] = 0.00
    return execution_dict

def clean_times(forecasts, file):

    xr_dataset = xarray.open_dataset(file)
    xr_dataset.load()
    valid_times = []

    for forecast in forecasts:
        # forecast is formatted like : "2024-03-19T00:00:00Z"
        # convert the string to a datetime object
        forecast_datetime = datetime.datetime.strptime(forecast, '%Y-%m-%dT%H:%M:%S.%fZ')
        # convert the datetime object to a numpy datetime64 object
        forecast_datetime = np.datetime64(forecast_datetime, 'ns')
        # append the forecast_datetime to the valid_times list
        valid_times.append(forecast_datetime)
    # drop all the valid_time that are not in the valid_times list
    for valid_time in xr_dataset.valid_time:
        if valid_time.values not in valid_times:
            try:
                xr_dataset = xr_dataset.drop_sel(valid_time=valid_time.values)
            except:
                pass
    return xr_dataset

def merge_xr(xr_list):
    # open the first file of the list
    xr_dataset = xr_list[0]
    # load data in memory
    xr_dataset.load()
    # loop over the xr_list
    for xr_ds in xr_list[1:]:
        # load data in memory
        xr_ds.load()
        # merge the two datasets
        xr_dataset = xarray.merge([xr_dataset, xr_ds])
    return xr_dataset

def main(params_variables, output_dir, execution_file, output_file, input_dir, config_file, params_time, metaparams):
    Logs = Exec_Logs()

    # start execution time
    start_time = time.time()
    attempts = 0
    successfull_attempts = 0

    # in parameters, search for the list_models
    with open(params_time, 'r') as f:
        json_dict = json.load(f)
        forecasts = json_dict['forecasts']

    # list all the files in the input directory
    files = os.listdir(input_dir)

    xr_list = []
    for file in files:
        input_file = input_dir + '/' + file
        try:
            xr_list.append(clean_times(forecasts, input_file))
        except:
            pass
    file_list = []
    attempts += 1
    try:
        xr_dataset = merge_xr(xr_list)
        output = os.path.join(output_dir, output_file)
        xr_dataset.to_netcdf(output)
        file_list.append(output_file)
        successfull_attempts += 1
    except:
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
    try:
        # with argparse, create a parser object
        parser = argparse.ArgumentParser()
        # the parameters are : --params_time, --params_variables, --output_dir, --execution_file
        
        parser.add_argument('--logs_file', type=str, help='Path to the execution file')
        parser.add_argument('--config_file', type=str, help='Path to the config file')
        parser.add_argument('--params_variables', type=str, help='Path to the variables parameters file')
        parser.add_argument('--params_time', type=str, help='Path to the time parameters file')
        parser.add_argument('--metaparams', type=str, help='Path to the metaparams file')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        parser.add_argument('--input_dir', type=str, help='Path to the input directory')
        parser.add_argument('--output_file', type=str, help='Name of the output file')
        
        # parse the arguments
        args = parser.parse_args()
        # assign the arguments to variables
        execution_file = args.logs_file
        config_file = args.config_file
        params_variables = args.params_variables
        params_time = args.params_time
        metaparams = args.metaparams
        output_dir = args.output_dir
        input_dir = args.input_dir
        output_file = args.output_file
        # call the main function
        main(params_variables, output_dir, execution_file, output_file, input_dir, config_file, params_time, metaparams)
    
    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_GFS.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)