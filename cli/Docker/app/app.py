# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import datetime
import os
import subprocess
import request_nwp as nwp
import request_obs as obs
import request_rea as rea
import build_request 
import inquirer
import json
import console
import time
from rich.console import Console
from rich.status import Status
import argparse

# parse the arguments : workdir params_folder metaparams_json params_time_json params_variables_json
parser = argparse.ArgumentParser()
parser.add_argument("--workdir", help="the working directory")
parser.add_argument("--params_folder", help="the parameters folder")
parser.add_argument("--metaparams_json", help="the metaparams json file")
parser.add_argument("--params_time_json", help="the params time json file")
parser.add_argument("--params_variables_json", help="the params variables json file")

args = parser.parse_args()

workdir = args.workdir
params_folder = args.params_folder
metaparams_json = args.metaparams_json
params_time_json = args.params_time_json
params_variables_json = args.params_variables_json

# execute the script with python app.py --workdir ./ --params_folder parameters --metaparams_json metaparams.json --params_time_json params_time.json --params_variables_json params_variables.json
params_path = os.path.join(workdir, params_folder)

# destroy all the files in './parameters/' directory with os.remove()
for file in os.listdir(params_path):
    if file is not None:
        os.remove(os.path.join(params_path, file))

# input what kind of datas needs to be agregated
dict_params, source_name, workflow_name = build_request.select_kind(workdir)
################ VARIABLES : SELECT VARIABLES ################
available_sources, source_path = build_request.get_available_sources(source_name, workdir)
# inupt how many requests needs to be agregated
nb_request = build_request.select_nb_requests(source_name)
# create the metaparams
json_metaparams = build_request.create_metaparams(dict_params, source_name, metaparams_json, workdir)

# loop for each request
data_paths = []
conf_paths = []
data_names = []
selected_variables = {}
name_file = params_variables_json
json_label = 'MODEL'
for i in range(nb_request):
    
    data_path, data_name, conf_path = build_request.select_data(source_name, available_sources, workdir)
    data_paths.append(data_path)
    conf_paths.append(conf_path)
    data_names.append(data_name)

    json_metaparams = build_request.set_metaparam(json_metaparams, source_name, json_label, data_name, True)

    if source_name == 'OBS':
        # append the selected variables to the dict
        selected_variables = obs.select_variables_OBS(conf_path)
        while not obs.confirm_variables_OBS(selected_variables, data_name):
            selected_variables = obs.select_variables_OBS(conf_path)
        build_request.write_json_air(params_path, selected_variables, name_file, append=data_name)
    elif source_name == 'NWP' or source_name == 'REANALYSIS' or source_name == 'SAT':
        # supress the selected data from the available sources
        available_sources.remove(data_name)
        selected_variables = nwp.select_variables_NWP(conf_path)
        while not nwp.confirm_variables_NWP(selected_variables, data_name):
            selected_variables = nwp.select_variables_NWP(conf_path)
        build_request.write_json_nwp(params_path, selected_variables, name_file, append=data_name)

json_label = 'STEP'
##############################################################
################ VARIABLES : SELECT LEVELS  ##################
if source_name == 'NWP' or source_name == 'REANALYSIS':
    levels, data = nwp.get_levels(params_path, name_file)
    if levels != {}:
        while not nwp.confirm_levels_NWP(levels):
            levels, data = nwp.get_levels(params_path, name_file)
        # write the json file
        with open(os.path.join(params_path, name_file), 'w') as outfile:
            json.dump(data, outfile, indent=4)

##############################################################
############################ TIME ############################
name_file = params_time_json
if source_name == 'OBS' or source_name == 'SAT':
    selected_observations = obs.global_obs_selection(conf_paths)
    while not obs.confirm_observation(selected_observations):
        selected_observations = obs.global_obs_selection(conf_paths)
elif source_name == 'REANALYSIS':
    selected_observations = rea.global_rea_selection(conf_paths)
    # selected_observations = {"start_time": "202411091000", "end_time": "202411090000"}
    # format the selected_observations for REANALYSIS : {"reanalysis_time": ["2024-07-18T00:00:00.000Z", "2024-07-18T01:00:00.000Z", "2024-07-18T02:00:00.000Z", "2024-07-18T03:00:00.000Z", "2024-07-18T04:00:00.000Z", "2024-07-18T05:00:00.000Z", "2024-07-18T06:00:00.000Z"]}
    start_time = datetime.datetime.strptime(selected_observations['start_time'], '%Y%m%d%H%M')
    end_time = datetime.datetime.strptime(selected_observations['end_time'], '%Y%m%d%H%M')
    reanalysis_time = []
    while start_time >= end_time:
        reanalysis_time.append(start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        start_time -= datetime.timedelta(hours=1)
    selected_observations = {'reanalysis_time': reanalysis_time}
    while not rea.confirm_observation(selected_observations):
        selected_observations = rea.global_rea_selection(conf_paths)
        start_time = datetime.datetime.strptime(selected_observations['start_time'], '%Y%m%d%H%M')
        end_time = datetime.datetime.strptime(selected_observations['end_time'], '%Y%m%d%H%M')
        reanalysis_time = []
        while start_time >= end_time:
            reanalysis_time.append(start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
            start_time -= datetime.timedelta(hours=1)
        selected_observations = {'reanalysis_time': reanalysis_time}
elif source_name == 'NWP':
    selected_day, selected_run_hour = nwp.select_day_and_run(conf_paths)
    selected_forecasts, option, dict_hours_by_model = nwp.select_common_forecast(conf_paths, selected_run_hour)
    if option == 'temporal interpolation':
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, json_label, 'interpolate-temporally', True)
    selected_observations = {'day': selected_day, 'run_hour': selected_run_hour, 'forecasts': selected_forecasts, 'option': option}
    # day : 20241115, run_hour : 00, forecasts : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # format the selected_observations for NWP : {"run_time": "2024-07-18T00:00:00.000Z", "forecasts": ["2024-07-18T00:00:00.000Z", "2024-07-18T01:00:00.000Z", "2024-07-18T02:00:00.000Z"]}
    run_time = datetime.datetime.strptime(selected_day + ' ' + selected_run_hour + ':00:00', '%Y%m%d %H:%M:%S')
    forecasts = []
    for forecast in selected_forecasts:
        forecasts.append((run_time + datetime.timedelta(hours=forecast)).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
    selected_observations = {'run_time': run_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), 'forecasts': forecasts}
    while not nwp.confirm_forecast(selected_observations):
        selected_day, selected_run_hour = nwp.select_day_and_run(conf_paths)
        selected_forecasts, option, dict_hours_by_model = nwp.select_common_forecast(conf_paths, selected_run_hour)
        selected_observations = {'day': selected_day, 'run_hour': selected_run_hour, 'forecasts': selected_forecasts, 'option': option}
        run_time = datetime.datetime.strptime(selected_day + ' ' + selected_run_hour + ':00:00', '%Y%m%d %H:%M:%S')
        forecasts = []
        for forecast in selected_forecasts:
            forecasts.append((run_time + datetime.timedelta(hours=forecast)).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
        selected_observations = {'run_time': run_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), 'forecasts': forecasts}


build_request.write_json(params_path, selected_observations, name_file)
##############################################################

if build_request.ask_merge():
    json_metaparams = build_request.set_metaparam(json_metaparams, source_name, json_label, 'MERGE', True)

if source_name == 'NWP' or source_name == 'REANALYSIS':
    if build_request.ask_spatial_interp():
        target_grid = nwp.select_grid_interpolation()
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, json_label, 'interpolate-spatially', True)
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, 'PARAMETER', 'grid', target_grid)

    if build_request.ask_box_lat_lon():
        western_lon,eastern_lon,southern_lat,northern_lat = nwp.select_box()
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, json_label, 'box', True)
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, 'PARAMETER', 'western_lon', float(western_lon))
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, 'PARAMETER', 'eastern_lon', float(eastern_lon))
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, 'PARAMETER', 'southern_lat', float(southern_lat))
        json_metaparams = build_request.set_metaparam(json_metaparams, source_name, 'PARAMETER', 'northern_lat', float(northern_lat))

# NWP to match API : FORECAST & REANALYSIS
if source_name == 'NWP':
    json_metaparams["SOURCE"] = "FORECAST"
if source_name == 'REANALYSIS':
    json_metaparams["SOURCE"] = "REANALYSIS"

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
# dump the json_metaparams into a file in the parameters directory
with open(os.path.join(params_path, metaparams_json), 'w') as outfile:
    json.dump(json_metaparams, outfile, indent=4)
