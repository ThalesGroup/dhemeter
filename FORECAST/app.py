# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import argparse
import os
import subprocess
import sys
import json
from utils import load_config, list_requested_data

FORECAST_APP_DIR = os.path.dirname(os.path.realpath(__file__))
FC_LIST = ['GFS','ICON_GLOBAL','ICON_EU','IFS','ARPEGE_EU','ARPEGE_GLOBAL','AROME_0025','AROME_001','AROME_PI_001','AROME_PI_0025']


def main(config_folder, instance_folder, share_folder):
    # in the config folder, we need to have a params_time.json, a params_variables.json and a metaparams.json
    # load the configuration
    params_time, params_variables, metaparams = load_config(config_folder)

    # metaparams has a "MODEL" key that contains the name of the data to use
    # make a list of all the data sources
    requested_data = list_requested_data(metaparams)
    print('Requested data:', requested_data)

    # metaparams has a "STEP" key that contains a "MERGE" key set to true or false
    # if true, we need to merge the data
    merge = metaparams['STEP']['MERGE']
    temporal_interpolation = metaparams['STEP']['interpolate-temporally']
    spatial_interpolation = metaparams['STEP']['interpolate-spatially']
    box = metaparams['STEP']['box']

    # if requested_data is empty, stop the program
    if not requested_data:
        print('No data requested')
        sys.exit(0)
    

    # else, if the data is in the list of the data sources
    # we can start the corresponding script
    for data in requested_data:
        if data in FC_LIST:
            print("Requesting : ", data)
            # call the script in pwd + ./REQUEST/ + data + /exec/docker_exec.sh instance_folder share_folder config_folder
            subprocess.run(['bash', FORECAST_APP_DIR + '/REQUEST/' + data + '/exec/docker_exec.sh', instance_folder, share_folder, config_folder])
        else:
            print('Data source not found:', data)
    if 'ICON_GLOBAL' in requested_data:
            # call the script in pwd + ./REMAP/exec/docker_exec.sh instance_folder share_folder config_folder
            subprocess.run(['bash', FORECAST_APP_DIR + '/REMAP/exec/docker_exec.sh', instance_folder, share_folder, config_folder, 'ICON_GLOBAL'])
    output_file_name = ''
    # if merge is true, we need to merge the data
    if merge:
        # call the script in pwd + ./MERGE/exec/docker_exec.sh instance_folder share_folder config_folder
        output_file_name = subprocess.run(['bash', FORECAST_APP_DIR + '/MERGE/exec/docker_exec.sh', instance_folder, share_folder, config_folder], capture_output=True).stdout.decode('utf-8').strip()
        print('Output file:', output_file_name)
        if temporal_interpolation:
            # call the script in pwd + ./INTERPOLATE/temporal/exec/docker_exec.sh instance_folder share_folder config_folder
            subprocess.run(['bash', FORECAST_APP_DIR + '/TIME_INTERP/exec/docker_exec.sh', instance_folder, share_folder, config_folder])
            # call the script in pwd + ./CLEAN_AND_MERGE/exec/docker_exec.sh instance_folder share_folder config_folder
            output_file_name = subprocess.run(['bash', FORECAST_APP_DIR + '/CLEAN_AND_MERGE/exec/docker_exec.sh', instance_folder, share_folder, config_folder], capture_output=True).stdout.decode('utf-8').strip()
            print('Output file:', output_file_name)
        if spatial_interpolation:
            # call the script in pwd + ./INTERPOLATE/spatial/exec/docker_exec.sh instance_folder share_folder config_folder output_file_name
            output_file_name = subprocess.run(['bash', FORECAST_APP_DIR + '/SPATIAL_INTERP/exec/docker_exec.sh', instance_folder, share_folder, config_folder, output_file_name], capture_output=True).stdout.decode('utf-8').strip()
            print('Output file:', output_file_name)
        if box:
            # call the script in pwd + ./BOX/exec/docker_exec.sh instance_folder share_folder config_folder output_file_name
            output_file_name = subprocess.run(['bash', FORECAST_APP_DIR + '/BOX/exec/docker_exec.sh', instance_folder, share_folder, config_folder, output_file_name], capture_output=True).stdout.decode('utf-8').strip()
            print('Final output file:', output_file_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agregateur de données')
    parser.add_argument('-c', '--config', help='dossier de configuration', required=True)
    parser.add_argument('-i', '--instance', help='Dossier de l\'instance d\'execution', required=True)
    parser.add_argument('-s', '--share', help='Dossier de partage', required=True)
    args = parser.parse_args()

    config_folder = args.config
    instance_folder = args.instance
    share_folder = args.share
    main(config_folder, instance_folder, share_folder)
