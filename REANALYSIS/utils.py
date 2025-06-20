import json
import os
import sys

def load_config(config_folder):
    try:
        with open(os.path.join(config_folder, 'params_time.json')) as f:
            params_time = json.load(f)
        with open(os.path.join(config_folder, 'params_variables.json')) as f:
            params_variables = json.load(f)
        with open(os.path.join(config_folder, 'metaparams.json')) as f:
            metaparams = json.load(f)
    except FileNotFoundError:
        print('Configuration file not found')
        print('params_time.json, params_variables.json and metaparams.json must be in the configuration folder')
        sys.exit(1)
    return params_time, params_variables, metaparams

def list_requested_data(metaparams):
    requested_data = []
    for data in metaparams['MODEL']:
        if metaparams['MODEL'][data]:
            requested_data.append(data)
    return requested_data