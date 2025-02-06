# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import requests
import datetime
import os
import subprocess
from lxml import etree as ET
import build_request

# input how many requests needs to be agregated
nb_request = build_request.select_nb_requests()
# loop for each request
for i in range(nb_request):
    # select the model
    model_path, model_name = build_request.select_source()
    # go to the xml file of the model
    model_xml = os.path.join(os.getcwd(),model_path, 'conf.xml')
    # name function build_request_+model_name
    f_request = getattr(build_request, 'build_request_' + model_name)
    print("model name: " + model_name)
    print("model path: " + model_path)
    #name container in lower case 
    container_name = 'request_' + model_name.lower()+':'+model_name.lower()
    
    try:
        request = f_request(model_xml)    
        '''
        # execute the function
        #IFS & GFS & GDAS
        #request = {'root': 'https://data.ecmwf.int/forecasts', 'run_hour': '00', 'date': '20230820', 'hour': '0'}
        #ERA5
        #request = {'type': 'reanalysis-era5-pressure-levels', 'variable': 'Temperature', 'level': '1000', 'year': '1980', 'month': '8', 'day': '20', 'hour': '12'}
        #ICON
        #request = {'root': 'https://opendata.dwd.de/weather/nwp/icon/grib', 'run_hour': '00', 'date': '20230822', 'hour': '000', 'var': 't', 'level_type': 'pressure-level', 'nb_lev': '1000'}
        #ICON_EU
        args = {'root': 'https://opendata.dwd.de/weather/nwp/icon-eu/grib/', 'run_hour': '12', 'date': '20230824', 'hour': '000', 'var': 't', 'level_type': 'pressure-level', 'nb_lev': '50'}
        '''
        # put request in a list to execute it with subprocess
        #arguments = ['docker', 'run', container_name, 'python3', 'request.py']
        #arguments = ['docker', 'run', '-d', container_name, 'python3', 'request.py']
        arguments = ['python3', 'request.py']
        for arg, value in request.items():
            arguments.append('--' + arg)
            arguments.append(value)
        print("request has been sent...")
        print(os.getcwd())
        # define the docker directory in the model directory
        docker_dir = os.path.join(os.getcwd(), model_path, 'Docker')
        print("docker directory: " + docker_dir)
        # change the working directory to the docker directory
        os.chdir(docker_dir)
        # execute the request
        subprocess.run(arguments)
        # return to the main directory
        os.chdir(os.path.join(os.getcwd(), '..', '..', '..'))
        # free 
        del model_path, model_name, docker_dir, arguments
    except:
        print("request is incorrect...")
        # hold the program
        input("Press enter to exit...")
        # exit the program
        exit()
