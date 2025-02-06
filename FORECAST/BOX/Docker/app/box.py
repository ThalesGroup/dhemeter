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

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'CREATE LAT LON BOX'
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

def main(input_file, input_dir, output_file, output_dir, execution_file, metaparams):
    Logs = Exec_Logs()
    # start execution time
    start_time = time.time()

    

    attempts = 0
    successfull_attempts = 0
    file_list = []

    # open the metaparams file
    with open(metaparams) as f:
        metaparams = json.load(f)

    western_longitude = metaparams["PARAMETER"]["western_lon"]
    eastern_longitude = metaparams["PARAMETER"]["eastern_lon"]
    southern_latitude = metaparams["PARAMETER"]["southern_lat"]
    northern_latitude = metaparams["PARAMETER"]["northern_lat"]

    input_ = os.path.join(input_dir, input_file)
    output_ = os.path.join(output_dir, output_file) 

    print('selecting the box')
    # print the coordinates of the box
    print('western_longitude:', western_longitude)
    print('eastern_longitude:', eastern_longitude)
    print('southern_latitude:', southern_latitude)
    print('northern_latitude:', northern_latitude)
    attempts += 1
    try:
        file_box = output_file
        remap_command = 'cdo sellonlatbox,'+str(western_longitude)+','+str(eastern_longitude)+','+str(southern_latitude)+','+str(northern_latitude)+' \
            ' + input_ + ' \
            ' + output_
        if os.system(remap_command) == 0:
            infos_command, ncdump_command = infos(file_box, output_dir)
            if os.system(infos_command + ' && ' + ncdump_command) == 0:
                successfull_attempts += 1
                file_list.append(file_box)
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
    try:
        # with argparse, create a parser object
        parser = argparse.ArgumentParser()
        
        # get the parameters from parser
        parser = argparse.ArgumentParser()
        parser.add_argument('--input_file', type=str)
        parser.add_argument('--input_dir', type=str)
        parser.add_argument('--output_file', type=str)
        parser.add_argument('--output_dir', type=str)
        parser.add_argument('--logs_file', type=str)
        parser.add_argument('--metaparams', type=str)
        args = parser.parse_args()

        # get the parameters from the parser
        input_file = args.input_file
        input_dir = args.input_dir
        output_file = args.output_file
        output_dir = args.output_dir
        execution_file = args.logs_file
        metaparams = args.metaparams

        main(input_file, input_dir, output_file, output_dir, execution_file, metaparams)

    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_GFS.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)
