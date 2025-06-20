import argparse
import subprocess
import os
import sys
import json
from utils import load_config, list_requested_data
import console
import time
from rich.console import Console
from rich.status import Status

REA_APP_DIR = os.path.dirname(os.path.realpath(__file__))
REA_LIST = ['ERA5_SINGLE_LEVEL', 'ERA5_PRESSURE_LEVELS']
SOURCE_TYPE = "REANALYSIS"

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
    print('Merge:', merge)

    # if requested_data is empty, stop the program
    if not requested_data:
        print('No data requested')
        sys.exit(0)
    
    console_request = Console()
    # create a status
    status = Status("Requesting data...", spinner="dots12", console=console_request)
    # start the status
    status.start()
    # else, if the data is in the list of the data sources
    # we can start the corresponding script
    STEP = "REQUEST"
    for data in requested_data:
        if data in REA_LIST:
            # call the script in pwd + ./REQUEST/ + data + /exec/docker_exec.sh instance_folder share_folder config_folder
            os.system('bash ' + REA_APP_DIR + '/REQUEST/' + data + '/exec/docker_exec.sh ' + instance_folder + ' ' + share_folder + ' ' + config_folder)
        else:
            print('Data source not found:', data)
    if console.docker_run(STEP, [item + ".log" for item in requested_data], instance_folder + "/logs", status):
        console.exec_table_nwp(STEP, [item + ".log" for item in requested_data], instance_folder + "/logs")
    # if merge is true, we need to merge the data
    if merge:
        STEP="MERGE"
        status = Status("Merging variables...", spinner="dots12", console=console_request)
        # start the status
        status.start()
        # call the script in pwd + ./MERGE/exec/docker_exec.sh instance_folder share_folder config_folder
        result = subprocess.run(
                                ['bash', f'{REA_APP_DIR}/MERGE/exec/docker_exec.sh', instance_folder, share_folder, config_folder],
                                capture_output=True,
                                text=True 
                            )
        lines = result.stdout.strip().splitlines()
        OUTPUT, LOGS_FILE, LOGS_DIR = lines[-3:]
    if console.docker_run(STEP, [LOGS_FILE], LOGS_DIR, status):
        console.exec_table(STEP, [LOGS_FILE], LOGS_DIR)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agregateur de données')
    parser.add_argument('-c', '--config', help='Configuration Folder', required=True)
    parser.add_argument('-i', '--instance', help='Exec instance Folder', required=True)
    parser.add_argument('-s', '--share', help='Shared Folder', required=True)
    args = parser.parse_args()

    config_folder = args.config
    instance_folder = args.instance
    share_folder = args.share
    main(config_folder, instance_folder, share_folder)