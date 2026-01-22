import cdsapi
import os
import argparse
import json
import time
import dotenv
import ERA5_PRESSURE_LEVEL 

def time_conversion(time):
    # time is a list of YYYY-MM-DDThh:mm:ssZ
    # make a list of YYYY, MM, DD, HH
    year = []
    month = []
    day = []
    hour = []
    # time is a list of YYYY-MM-DDThh:mm:ssZ
    for i in range(len(time)):
        if time[i][:4] not in year:
            year.append(time[i][:4])
        if time[i][5:7] not in month:
            month.append(time[i][5:7])
        if time[i][8:10] not in day:
            day.append(time[i][8:10])
        if time[i][11:16] not in hour:
            hour.append(time[i][11:16])

    return year, month, day, hour

# create a function to read he coordinates from the metaparameters file
def read_coordinates(metaparams):
    with open(metaparams, 'r') as f:
        meta_params = json.load(f)
        meta_params = meta_params['PARAMETER']
        # if all 4 coordinates are given and are floats, use them
        if 'western_lon' in meta_params and 'eastern_lon' in meta_params and 'southern_lat' in meta_params and 'northern_lat' in meta_params:
            if isinstance(meta_params['western_lon'], float) and isinstance(meta_params['eastern_lon'], float) and isinstance(meta_params['southern_lat'], float) and isinstance(meta_params['northern_lat'], float):
                western_lon = meta_params['western_lon']
                eastern_lon = meta_params['eastern_lon']
                southern_lat = meta_params['southern_lat']
                northern_lat = meta_params['northern_lat']
                return western_lon, eastern_lon, southern_lat, northern_lat
    return -180, 180, -90, 90

# create the function to give parameters to the cdsapi.Client()
def Create_ERA5_Pressure_Levels_Request(name_variables, rea_hours, levels, output_dir, file_name, western_lon, eastern_lon, southern_lat, northern_lat):
    print(rea_hours)
    year, month, day, hour = time_conversion(rea_hours)
    print(year, month, day, hour)
    # create the client
    c = cdsapi.Client()

    # create the request
    try:
        request = c.retrieve(
            'reanalysis-era5-pressure-levels',
            {
                'product_type': 'reanalysis',
                'variable': name_variables,
                'year': year,
                'month': month,
                'day': day,
                'time': hour,
                'pressure_level': levels,
                'format': 'grib',
                'area':[northern_lat, western_lon, southern_lat, eastern_lon]
            },
            os.path.join(output_dir, file_name))
        return True
    except:
        return False

# function to trace the execution of the script
def Exec_Logs():
    # create an empty dict with the keys 'execution_status', 'attempts' and 'successfull_attempts', 'file_list'
    execution_dict = {}
    execution_dict['Data_name'] = 'ERA5_PRESSURE_LEVELS'
    execution_dict['execution_status'] = 0 # request started
    execution_dict['attempts'] = 0
    execution_dict['successfull_attempts'] = 0
    execution_dict['file_list'] = []
    execution_dict['execution_time'] = 0.00
    return execution_dict

def main(params_time, params_vars, output_dir, execution_file, metaparams):
    # Load environment variables
    dotenv.load_dotenv()
   # create the execution logs
    Logs = Exec_Logs()

    # start execution time
    start_time = time.time()
    attempts = 0
    successfull_attempts = 0

    with open(params_vars, 'r') as f:
        json_file = json.load(f)
        if json_file['ERA5_PRESSURE_LEVELS']['variables'] == []:
            Logs['execution_status'] = 40 # no variables selected
            # dump the dict into a json file /execution/logs_XXXX.json
            with open(execution_file, 'w') as logs:
                json.dump(Logs, logs, indent=4)
            exit()

    with open(params_time, 'r') as f:
        json_file = json.load(f)
        if json_file['reanalysis_time'] == []:
            Logs['execution_status'] = 41 # no forecasts selected
            # dump the dict into a json file /execution/logs_XXXXX.json
            with open(execution_file, 'w') as logs:
                json.dump(Logs, logs, indent=4)
            exit()

    file_list = []

    with open(params_time, 'r') as f:
        params_time = json.load(f)
        # retrieve the start_time and end_time values
        rea_hours = params_time['reanalysis_time']

    with open(params_vars, 'r') as f:
        params_variables = json.load(f)
        # retrieve the variables values
        dict_variables = params_variables['ERA5_PRESSURE_LEVELS']['variables']
        name_variables = []
        pressure_levels = []
        for variable in dict_variables:
            name_variable = variable['variable']
            name_variables.append(name_variable)
            levels = variable['levels']
            # if a level in levels is new to pressure_levels, add it
            for level in levels:
                if level not in pressure_levels:
                    pressure_levels.append(level)
    
    # read the metaparameters file to get the lat lon coordinates
    western_lon, eastern_lon, southern_lat, northern_lat = read_coordinates(metaparams)
    print(western_lon, eastern_lon, southern_lat, northern_lat)

    # create the file name with the first time and the last time
    first_hour = rea_hours[0]
    last_hour = rea_hours[-1]
    file_name = "ERA5_PRESSURE_LEVELS_" + first_hour + "_" + last_hour + ".grib2"
    attempts += 1
    # create the request
    if Create_ERA5_Pressure_Levels_Request(name_variables, rea_hours, pressure_levels, output_dir, file_name, western_lon, eastern_lon, southern_lat, northern_lat):
        successfull_attempts += 1
        file_list.append(file_name)

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
        parser.add_argument('--output_dir', type=str, help='Path to the output directory')
        parser.add_argument('--metaparams', type=str, help='Path to the metaparameters file')

        # parse the arguments
        args = parser.parse_args()
        
        # assign the arguments to variables
        execution_file = args.logs_file
        config_file = args.config_file
        params_time = args.params_time
        params_vars = args.params_variables
        metaparams = args.metaparams
        output_dir = args.output_dir
        
        
        main(params_time, params_vars, output_dir, execution_file, metaparams)
    except:
        Logs = Exec_Logs()
        Logs['execution_status'] = 50
        # dump the dict into a json file /execution/logs_XXXX.json
        with open(execution_file, 'w') as logs:
            json.dump(Logs, logs, indent=4)
