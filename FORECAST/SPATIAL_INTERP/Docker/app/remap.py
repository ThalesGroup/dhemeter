# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import os
import json
import time
import argparse
from gen_map import gen_map_region, gen_map_world

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'SPATIAL INTERPOLATION'
    execution_dict['execution_status'] = 0 #request started
    execution_dict['attempts'] = 0 
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict

def infos(file_name, output_dir):
    infos_command = 'cdo -info ' + output_dir + '/' + file_name
    ncdump_command = 'ncdump -h ' + output_dir + '/' + file_name
    return infos_command, ncdump_command

def main(input_dir, input_file, metaparams, output_dir, output_file, execution_file):
    Logs = Exec_Logs()
    # start execution time
    start_time = time.time()

    attempts = 0
    successfull_attempts = 0
    file_list = []

    # load the metaparams file and extract the target grid
    with open(metaparams) as f:
        metaparams = json.load(f)
        precision = metaparams["PARAMETER"]['grid']
        western_lon = metaparams["PARAMETER"]['western_lon']
        eastern_lon = metaparams["PARAMETER"]['eastern_lon']
        southern_lat = metaparams["PARAMETER"]['southern_lat']
        northern_lat = metaparams["PARAMETER"]['northern_lat']
    # if the precision is a float between 0 and 1, generate a map for the world
    if isinstance(precision, float) and 0 < precision < 1:
        # generate the map for the target grid : if the western_lon, eastern_lon, southern_lat and northern_lat are not float, the function will return a map for the world
        if isinstance(western_lon, float) and isinstance(eastern_lon, float) and isinstance(southern_lat, float) and isinstance(northern_lat, float):
            print('region')
            target_grid = gen_map_region(precision, western_lon, eastern_lon, southern_lat, northern_lat, output_dir)
        else:
            print('world')
            target_grid = gen_map_world(precision, output_dir)

    # try to remap the file with the target grid
    attempts += 1
    try:
        filename = input_file
        file_remaped = output_file
        remap_command = 'cdo -remapbil,' + target_grid + ' ' + input_dir + '/' + filename + ' ' + output_dir + '/' + file_remaped
        if os.system(remap_command) == 0:
            infos_command, ncdump_command = infos(file_remaped, output_dir)
            if os.system(infos_command + ' && ' + ncdump_command) == 0:
                successfull_attempts += 1
                file_list.append(file_remaped)
            else:
                raise Exception('Error in remapping the file')
        else:
            raise Exception('Error in remapping the file')
    except Exception:
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
    #try:
        # with argparse, create a parser object
        parser = argparse.ArgumentParser()
        
        # the parameters are : --input_dir, --input_file, --target_grid, --output_dir, --output_file, --execution_file
        parser.add_argument('--logs_file', type=str, help='Path to the execution file')
        parser.add_argument('--input_dir', type=str, help='Path to the input directory')
        parser.add_argument('--input_file', type=str, help='Name of the input file')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        parser.add_argument('--output_file', type=str, help='Name of the output file')
        parser.add_argument('--metaparams', type=str, help='metaparams file')
        # parse the arguments
        args = parser.parse_args()
        
        # assign the arguments to variables
        input_dir = args.input_dir
        input_file = args.input_file
        metaparams = args.metaparams
        output_dir = args.output_dir
        output_file = args.output_file
        execution_file = args.logs_file
        
        main(input_dir, input_file, metaparams, output_dir, output_file, execution_file)

'''except:
Logs = Exec_Logs()
Logs['execution_status'] = 50
# dump the dict into a json file /execution/logs_GFS.json
with open(execution_file, 'w') as logs:
    json.dump(Logs, logs, indent=4)'''
