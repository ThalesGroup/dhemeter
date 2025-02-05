import requests
import os
import argparse
import json
import time
import datetime
# function to retrieve data from ECMWF server based on url path given
def Create_URL_IFS (root, run_hour, date, hour):
    url = root + '/' + date + '/' + run_hour + 'z/ifs/0p25/oper/' + date + run_hour + '0000-' + hour + 'h-oper-fc.grib2'
    return url

def get_interp_hours(selected_hours, IFS_fc_hours):
    # selected hours is a list of hours for which we want to retrieve data
    # IFS_fc_hours is a list of forecast hours theoretically available for the IFS model
    # if the selected hours are not in the IFS_fc_hours list, we need to select the 2 closest hours lower and upper
    common_hours = []
    for fc_hour in selected_hours:
        if fc_hour in IFS_fc_hours:
            if str(fc_hour) not in common_hours:
                common_hours.append(str(fc_hour))
        else:
            nearest_lower = max(filter(lambda x: x < fc_hour, IFS_fc_hours))
            nearest_upper = min(filter(lambda x: x > fc_hour, IFS_fc_hours))
            if str(nearest_lower) not in common_hours:
                common_hours.append(str(nearest_lower))
            if str(nearest_upper) not in common_hours:
                common_hours.append(str(nearest_upper))
    return common_hours

def create_hours_list(HOURS, run_hour):
    hours = []
    for run in HOURS['run_hour']:
        if run["value"] == int(run_hour):
            # calculate a list of hours for the selected run
            hours_steps = run['Hours_Steps']
            for step in hours_steps['step']:
                min = step['min']
                max = step['max']
                increment = step['value']
                for i in range(min, max+1, increment):
                    hours.append(i)
    return hours
            

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'IFS'
    execution_dict['execution_status'] = 0 # request started
    execution_dict['attempts'] = 0
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict

# params_variables = './parameters/params_variables.json'
# params_time = './parameters/params_time.json'
# execution_file = './execution/logs_IFS.json'
# output_dir = './output/'
def main(params_time, params_variables, output_dir, execution_file, config_file, metaparams):
    Logs = Exec_Logs()

    # start execution time
    start_time = time.time()

    with open(params_variables, 'r') as f:
        json_file = json.load(f)
        if json_file['IFS']['variables'] == []:
            Logs['execution_status'] = 40 # no variables selected
            # dump the dict into a json file /execution/logs_IFS.json
            with open(execution_file, 'w') as logs:
                json.dump(Logs, logs, indent=4)
            exit()

    with open(params_time, 'r') as f:
        json_file = json.load(f)
        if json_file['forecasts'] == []:
            Logs['execution_status'] = 41 # no forecasts selected
            # dump the dict into a json file /execution/logs_IFS.json
            with open(execution_file, 'w') as logs:
                json.dump(Logs, logs, indent=4)
            exit()
    with open(metaparams, 'r') as f:
        json_file = json.load(f)
        if not json_file['MODEL']['IFS']:
            Logs['execution_status'] = 42
            # dump the dict into a json file /execution/logs_ICON_EU.json
            with open(execution_file, 'w') as logs:
                json.dump(Logs, logs, indent=4)
            exit()

    attempts = 0
    successfull_attempts = 0
    file_list = []

    root = 'https://data.ecmwf.int/forecasts'
    # with json, open the 'params_time.json' file and find the start_time and end_time values
    model_name = 'IFS'
    option = 'native'
    with open(metaparams, 'r') as f:
        metaparams = json.load(f)
        # in 'STEP' key, find the 'interpolate-temporally' key
        if metaparams['STEP']['interpolate-temporally']:
            option = 'temporal interpolation'
    print('Option:', option)
    with open(params_time, 'r') as f:
        params_time = json.load(f)
        run_time = datetime.datetime.strptime(params_time['run_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # run hour with format "HH" (00, 06, 12, 18)
        run_hour = run_time.strftime('%H').zfill(2)
        date = run_time.strftime('%Y%m%d')
        with open(config_file) as f:
            meta = json.load(f)
            # depending on the run hour, retrieve the forecast hours
            # search for a MODEL with "_name" key is equal to IFS
            for model in meta['config']['SOURCES']['NWP']['MODEL']:
                if model['_name'] == model_name:
                    HOURS = model['run_hours']
                    break
        MODEL_FC_HOURS = create_hours_list(HOURS, run_hour)
        selected_forecasts = params_time['forecasts']
        # calculate the difference between the run_time and the selected forecasts
        selected_hours = []
        for forecast in selected_forecasts:
            forecast_time = datetime.datetime.strptime(forecast, '%Y-%m-%dT%H:%M:%S.%fZ')
            # calculate the difference between the forecast time and the run time in hours
            diff = forecast_time - run_time
            hours = diff.days * 24 + diff.seconds // 3600
            selected_hours.append(hours)
        # open the metadata file and retrieve hours for the selected forecasts
        
        # create a list of forecast times
        hours = []
        # in one line, append to the list the forecast times
        if option != 'temporal interpolation':
            for forecast in selected_hours:
                hours.append(str(forecast))
        else:
            hours = get_interp_hours(selected_hours, MODEL_FC_HOURS)
        for hour in hours:
            url = Create_URL_IFS(root, run_hour, date, hour)
            attempts += 1
            try:
                print('start requesting at url:', url)
                r = requests.get(url, allow_redirects=True)
                if r.status_code != 200:
                    raise Exception('File not available')
                else:
                    filename = 'IFS_' + date + '_' + run_hour + '_' + hour + '.grib2'
                    file_path = os.path.join(output_dir, filename)
                    open(file_path, 'wb').write(r.content)
                    file_list.append(filename)
                    successfull_attempts += 1
            except:
                print('No data available for the request : ' + url)

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
        parser.add_argument('--config_file', type=str, help='Path to the configuration file')
        parser.add_argument('--params_time', type=str, help='Path to the time parameters file')
        parser.add_argument('--params_variables', type=str, help='Path to the variables parameters file')
        parser.add_argument('--metaparams', type=str, help='Path to the metadata file')
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        # parse the arguments
        args = parser.parse_args()
        # assign the arguments to variables
        params_time = args.params_time
        params_variables = args.params_variables
        output_dir = args.output_dir
        logs_file = args.logs_file
        metaparams = args.metaparams
        config_file = args.config_file
        # check if the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        main(params_time, params_variables, output_dir, logs_file, config_file, metaparams)
    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_IFS.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)