import os
import json
import xarray
import time
import argparse

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'NWP'
    execution_dict['execution_status'] = 0 # request started
    execution_dict['attempts'] = 0
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict

def detect_mode(metadata, model_name):
    # metadata is an json file containing the metadata of the models
    # model_name is the name of the model
    # the function returns the mode of the model
    # the mode is the retrieval type of the model (all, single, custom)
    with open(metadata, 'r') as f:
        json_dict = json.load(f)
    # the name of the model is at the same level as the mode
    tab_nwp = json_dict["config"]["SOURCES"]["NWP"]["MODEL"]
    for nwp in tab_nwp:
        if nwp["_name"] == model_name:
            mode = nwp["_mode"]
    return mode

def extract_data(model_names, files, input_dir, params_vars, config_file):
    grib_files = {}
    xr_data = []
    xr_dataset = xarray.Dataset()

    attempts = 0
    
    for model_name in model_names:
        model_files = []
        for file in files:
            # if file contains the model name and is a grib or netcdf file
            if model_name in file and (file.endswith('.grib') or file.endswith('.nc') or file.endswith('.grib2')):
                model_files.append(file)
        grib_files[model_name] = model_files
    for model_name in model_names:
        with open(params_vars, 'r') as f:
            params_variables = json.load(f)
            list_variables = params_variables[model_name]['variables']
            for variable in list_variables:
                variable_name = variable['variable']
                variable_level = variable['level_type']
                level_type_name = variable['level_type_name']
                for file in grib_files[model_name]:
                    unique_var_lev_file = variable_name + '_'+ variable_level + '_' + level_type_name
                    if unique_var_lev_file in file and detect_mode(config_file, model_name) == 'single':
                        try:
                            attempts += 1
                            # if the file is a grib file then use the cfgrib engine
                            print("path to file ", os.path.join(input_dir, file))
                            xr_var = xarray.open_dataset(os.path.join(input_dir, file), engine='cfgrib')
                            # if it's a netcdf file grib file then use the netcdf engine
                            xr_var = xarray.open_dataset(os.path.join(input_dir, file))
                            single_variable_name = xr_var.data_vars.__iter__().__next__()
                            _name = variable_name + '_' + model_name
                            xr_var = xr_var.rename({single_variable_name: _name})
                            xr_var = xr_var.rename({'latitude': 'lat'+ '_' + model_name})
                            xr_var = xr_var.rename({'longitude': 'lon'+ '_' + model_name})
                            xr_var = xr_var.drop(['time', 'step'])
                            # an attribute "model" = model_name to the variable
                            xr_var[_name].attrs['model'] = model_name
                            xr_var.attrs['model'] = model_name
                            print(xr_var[_name].name)
                            try:
                                xr_var = xr_var.expand_dims(['valid_time', level_type_name])
                                print("extended valid time")
                                print("extended dimension level : " + level_type_name)
                            except:
                                xr_var = xr_var.expand_dims(['valid_time'])
                                print("extended valid time")
                            #if level_type_name in xr_var[_name].dims:
                            xr_data.append(xr_var)
                            print("appended")
                            
                        except:
                            print('the variable ' + variable_name + ' from the model '+model_name+' is not available at the moment')
                    elif detect_mode(config_file, model_name) == 'global' or detect_mode(config_file, model_name) == 'custom':
                        try:
                            attempts += 1
                            print(os.path.join(input_dir, file))
                            kwargs = {'filter_by_keys':{'typeOfLevel': level_type_name, 'shortName': variable_name}}
                            xr_var = xarray.open_dataset(os.path.join(input_dir, file), engine='cfgrib', backend_kwargs=kwargs)
                            print(xr_var.data_vars)
                            variable_name_ = xr_var.data_vars.__iter__().__next__()
                            _name = variable_name + '_' + model_name
                            xr_var = xr_var.rename({variable_name_: _name})
                            if variable['levels'] is not None:
                                levels = variable['levels']
                                kwargs = {level_type_name: levels}
                                xr_var = xr_var.sel(**kwargs)
                            xr_var = xr_var.rename({'latitude': 'lat'+ '_' + model_name})
                            xr_var = xr_var.rename({'longitude': 'lon'+ '_' + model_name})
                            xr_var = xr_var.drop(['time', 'step'])
                            # an attribute "model" = model_name to the variable
                            xr_var[_name].attrs['model'] = model_name
                            xr_var.attrs['model'] = model_name
                            # print the name of the var
                            print(xr_var[_name].name)
                            try:
                                xr_var = xr_var.expand_dims(['valid_time', level_type_name])
                                print("extended valid time")
                                print("extended dimension level : " + level_type_name)
                            except:
                                xr_var = xr_var.expand_dims(['valid_time'])
                                print("extended valid time")
                            #if level_type_name in xr_var[_name].dims:
                            xr_data.append(xr_var)
                            print("appended")
                        except:
                            print('the variable ' + variable_name + ' from the model '+model_name+' is not available at the moment')
    return xr_data, attempts


def order_data(xr_data, config_file):
    # loop over the xr_data list and get the attribute 'model' of each variable
    # append the list of the models
    # and then order the list depending on the "order" attribute of the metadata file
    with open(config_file, 'r') as f:
        metadata = json.load(f)
    tab_nwp = metadata["config"]["SOURCES"]["NWP"]["MODEL"]
    model_order = {}
    for xr in xr_data:
        # if the model is not already in the list, then append it
        if xr.attrs['model'] not in model_order:
            # create the key with the model name and the value with the order
                for nwp in tab_nwp:
                    if nwp["_name"] == xr.attrs['model']:
                        print(nwp)
                        model_order[xr.attrs['model']] = nwp["_order"]

    # sort the list of models
    sorted_models = sorted(model_order.items(), key=lambda x: x[1])
    print(sorted_models)
    # order the list of xr_data
    ordered_xr_data = []
    for model in sorted_models:
        for xr in xr_data:
            if xr.attrs['model'] == model[0]:
                ordered_xr_data.append(xr)
    return ordered_xr_data

    
def merge_data(xr_data, attempts):
    successfull_attempts = 0
    xr_dataset = xarray.Dataset()
    print("xr_dataset", xr_dataset)
    for xr in xr_data:
        try:
            if not xr_dataset.notnull().all():
                xr_dataset = xr
            else:
                xr_dataset = xarray.merge([xr_dataset, xr])
            successfull_attempts += 1
        except:
            print('Error in merging the data')
    print("xr_dataset", xr_dataset)
    return xr_dataset, successfull_attempts

def write_netcdf(xr_dataset, file_name, output_dir):
    output_file = os.path.join(output_dir, file_name)
    try:
        xr_dataset.to_netcdf(output_file)
        execution_status = 20 # successfull execution
    except:
        execution_status = 50 # Error in request
    return execution_status


def main(params_variables, output_dir, execution_file, output_file, input_dir, config_file, params_time, metaparams):
    Logs = Exec_Logs()
    # start execution time
    start_time = time.time()
    option = 'native'
    list_models = []
    with open(metaparams, 'r') as f:
        metaparams = json.load(f)
        # in 'STEP' key, find the 'interpolate-temporally' key
        if metaparams['STEP']['interpolate-temporally']:
            option = 'temporal interpolation'
        for model in metaparams['MODEL']:
            if metaparams['MODEL'][model]:
                list_models.append(model)
    print('Option:', option)
    print('models : ', list_models)
    files = os.listdir(input_dir)
    if option != 'temporal interpolation':
        if files != []:
            attempts = 0
            successfull_attempts = 0
            file_name = output_file
            xr_data, attempts = extract_data(list_models, files, input_dir, params_variables, config_file)
            xr_data = order_data(xr_data, config_file)
            print("xr_data ordered", xr_data)
            xr_dataset, successfull_attempts = merge_data(xr_data, attempts)
            print("xr_dataset", xr_dataset)
            # if the xr_dataset is not empty, write the netcdf file
            if xr_dataset:
                Logs['execution_status'] = write_netcdf(xr_dataset, file_name, output_dir)
            else:
                print('No data to merge')
            if Logs['execution_status'] == 20:
                Logs['file_list'].append(file_name)
            Logs['attempts'] = attempts
            Logs['successfull_attempts'] = successfull_attempts
        else:
            Logs['execution_status'] = 24
    else:
        if files != []:
            attempts = 0
            successfull_attempts = 0
            for model in list_models:
                file_name = model + '_' + output_file
                xr_data, attempts_model = extract_data([model], files, input_dir, params_variables, config_file)
                xr_data = order_data(xr_data, config_file)
                print("xr_data ordered", xr_data)
                attempts += attempts_model
                xr_dataset, successfull_attempts_model = merge_data(xr_data, attempts)
                print("xr_dataset", xr_dataset)
                # if the xr_dataset is not empty, write the netcdf file
                if xr_dataset:
                    Logs['execution_status'] = write_netcdf(xr_dataset, file_name, output_dir)
                else:
                    print('No data to merge')
                if Logs['execution_status'] == 20:
                    Logs['file_list'].append(file_name)
                    successfull_attempts += successfull_attempts_model
            
            Logs['attempts'] = attempts
            Logs['successfull_attempts'] = successfull_attempts
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
        logs_file = args.logs_file
        config_file = args.config_file
        params_variables = args.params_variables
        params_time = args.params_time
        metaparams = args.metaparams
        output_dir = args.output_dir
        input_dir = args.input_dir
        output_file = args.output_file
        # call the main function
        main(params_variables, output_dir, logs_file, output_file, input_dir, config_file, params_time, metaparams)
    

    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_GFS.json
        with open(logs_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)