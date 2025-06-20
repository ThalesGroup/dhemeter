import os
import json
import xarray
import time
import argparse
import numpy as np
import pandas as pd
import datetime


# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'REANALYSIS'
    execution_dict['execution_status'] = 0 # request started
    execution_dict['attempts'] = 0
    execution_dict['successfull_attempts'] = 0
    execution_dict['execution_time'] = 0.00
    return execution_dict

# Create a function to extract the data from the grib files for full coherence Mode 
def aggregation_REA(model_names, files, attempts, successfull_attempts, output_dir, output_file, params_vars, reanalysis_time):
    grib_files = {}
    xr_data = []
    xr_dataset = xarray.Dataset()
    
    for model_name in model_names:
        model_files = []
        for file in files:
            if file.startswith(model_name) and file.endswith('.grib2') or file.endswith('.grib'):
                model_files.append(file)
        grib_files[model_name] = model_files
    
    # cast the reanalysis_time from iso format to datetime
    reanalysis_time = pd.to_datetime(reanalysis_time)
    print(reanalysis_time)
    for model_name in model_names:
        with open(params_vars, 'r') as f:
            params_variables = json.load(f)
            list_variables = params_variables[model_name]['variables']
            for file in grib_files[model_name]:
                for variable in list_variables:
                    variable_name = variable['variable']
                    variable_desc = variable['description']
                    level_type_name = variable['level_type_name']
                    
                    xr_var = xarray.open_dataset(
                                                filename_or_obj= input_dir + '/' + file,
                                                engine='cfgrib',
                                                backend_kwargs=
                                                {
                                                    'filter_by_keys':
                                                    {
                                                        'typeOfLevel': level_type_name,
                                                        'name': variable_desc
                                                    }
                                                }
                                                )
                    if not xr_var.variables:
                        pass
                    else:
                        if 'time' in xr_var.dims and 'step' in xr_var.dims:
                            xr_var = xr_var.stack(valid_time=['time', 'step'])
                            # reset index valid_time
                            xr_var = xr_var.reset_index('valid_time')
                            # reassign time + steps coordinates
                            xr_var = xr_var.assign_coords(valid_time=xr_var.time + xr_var.step)
                        elif 'time' in xr_var.dims:
                            # delete valid_time and step coordinate
                            xr_var = xr_var.drop('valid_time')
                            xr_var = xr_var.drop('step')
                            # rename time coordinate to valid_time
                            xr_var = xr_var.rename({'time': 'valid_time'})
                            # create a time coordinate depending on valid time
                            xr_var = xr_var.assign_coords(time=xr_var.valid_time)
                            xr_var = xr_var.drop('time')
                        elif 'step' in xr_var.dims:
                            # make time a coordinate
                            xr_var = xr_var.expand_dims('time')
                            xr_var = xr_var.stack(valid_time=['time', 'step'])
                            # reset index valid_time
                            xr_var = xr_var.reset_index('valid_time')
                            # reassign time + steps coordinates
                            xr_var = xr_var.assign_coords(valid_time=xr_var.time + xr_var.step)
                        elif 'valid_time' in xr_var.dims:
                            xr_var = xr_var
                        else:
                            xr_var = xr_var.expand_dims('time')
                            xr_var = xr_var.expand_dims('step')
                            xr_var = xr_var.stack(valid_time=['time', 'step'])
                            # reset index valid_time
                            xr_var = xr_var.reset_index('valid_time')
                            # reassign time + steps coordinates
                            xr_var = xr_var.assign_coords(valid_time=xr_var.time + xr_var.step)
                        print(xr_var)
                        try:
                            xr_var = xr_var.sel(valid_time=reanalysis_time)
                            xr_var = xr_var.expand_dims([level_type_name])
                        except:
                            print("Previously Dimensionned dataset")
                        xr_data.append(xr_var)
    print("xr_data : ", xr_data)
    if xr_data != []:
        for xr in xr_data:
            # if the xr_dataset is empty, we need to create it with the xr
            attempts += 1
            try:
                if not xr_dataset.notnull().all():
                    xr_dataset = xr
                else:
                    xr_dataset = xarray.merge([xr_dataset, xr])
                successfull_attempts += 1
            except:
                pass
    else:
        execution_status = 24
    # xr_dataset to netcdf
    try:
        xr_dataset.to_netcdf(output_dir + '/' + output_file)
        execution_status = 20
    except:
        execution_status = 25
    return attempts, successfull_attempts, execution_status

def main(params_variables, params_time, output_dir, execution_file, input_dir, output_file):
    Logs = Exec_Logs()

    # start execution time
    start_time = time.time()
    attempts = 0
    successfull_attempts = 0

    # in parameters, search for the list_models
    with open(params_variables, 'r') as f:
        json_dict = json.load(f)
        list_models = json_dict.keys()
    with open(params_time, 'r') as f:
        json_dict = json.load(f)
        list_times = json_dict["reanalysis_time"]
    list_times = [np.datetime64(i) for i in list_times]
    files = os.listdir(input_dir)
    if files != []:
        Logs['attempts'], Logs['successfull_attempts'], Logs['execution_status'] = aggregation_REA(list_models, files, attempts, successfull_attempts, output_dir, output_file, params_variables, list_times)
    else:
        Logs['execution_status'] = 24

    # end execution time
    end_time = time.time()
    execution_time = end_time - start_time
    Logs['execution_time'] = round(execution_time, 2)

    # dump the dict into a json file /execution/logs_GFS.json
    with open(execution_file, 'w') as logs:
        json.dump(Logs, logs, indent=4)

if __name__ == '__main__':
    try:
        # with argparse, create a parser object
        parser = argparse.ArgumentParser()
        
        # the parameters are : --params_variables, --output_dir, --execution_file, input_dir
        parser.add_argument('--execution_file', type=str, help='Path to the execution file')
        parser.add_argument('--params_variables', type=str, help='Path to the variables parameters file')
        parser.add_argument('--params_time', type=str, help='Path to the time parameters file')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        parser.add_argument('--output_file', type=str, help='Name of the output file')
        parser.add_argument('--input_dir', type=str, help='Path to the input directory')
        
        # parse the arguments
        args = parser.parse_args()
        
        # assign the arguments to variables
        execution_file = args.execution_file
        params_variables = args.params_variables
        params_time = args.params_time
        output_dir = args.output_dir
        output_file = args.output_file
        input_dir = args.input_dir
        
        # call the main function
        main(params_variables, params_time, output_dir, execution_file, input_dir, output_file)
    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_XXXX.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)