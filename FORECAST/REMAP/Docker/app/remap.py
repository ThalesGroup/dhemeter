# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import os
import json
import time
import argparse

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'ICON_REMAP'
    execution_dict['execution_status'] = 0 #request started
    execution_dict['attempts'] = 0 
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict


def main(output_dir, execution_file, logs_params, input_dir, option):
    Logs = Exec_Logs()
    # start execution time
    start_time = time.time()

    logs_path = logs_params
    with open(logs_path) as json_file:
        logs = json.load(json_file)
        files = logs['file_list']

    attempts = 0
    successfull_attempts = 0
    file_list = []

    for file in files:
        filename = file
        # must have remaped in the beginning of the filename
        filename_remaped = 'remaped_' + filename
        attempts += 1
        try:
            print(os.getcwd())
            print(os.listdir())
            os.system("ls raw")
            remap_command = 'cdo -f grb2 remap,/data/target_grid_' + option + '.txt,weights_' + option + '.nc ' + input_dir + '/' + filename + ' ' + output_dir + '/' + filename_remaped
            print(remap_command)
            os.system(remap_command)
            os.remove(input_dir + filename)
            successfull_attempts += 1
            file_list.append(filename_remaped)
        except:
            if os.path.exists(input_dir + filename):
                os.remove(input_dir + filename)
            else:
                pass


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
        parser.add_argument('--logs_params', type=str, help='Path to the logs parameters file')
        parser.add_argument('--input_dir', type=str, help='Path to the input directory')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        parser.add_argument('--option', type=str, help='Option to choose the type of remap')
        
        # parse the arguments
        args = parser.parse_args()
        
        # assign the arguments to variables
        output_dir = args.output_dir
        input_dir = args.input_dir
        execution_file = args.logs_file
        logs_params = args.logs_params
        option = args.option

        main(output_dir, execution_file, logs_params, input_dir, option)
    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_GFS.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)
