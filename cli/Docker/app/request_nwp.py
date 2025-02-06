# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
import lxml.etree as ET
import os
import datetime
import requests
import subprocess
import calendar
import inquirer
import json
from rich.console import Console
from rich.table import Table

################################################################
########################  VARIABLES NWP  #######################
################################################################

def select_variables_NWP(NWP_path):
    selected_variables= {}
    root, class_name, model_name = get_config_paths(NWP_path)

    # select the variable in class, model, variables, variable
    # variables takes key value (name, description)
    list_variables = []
    variables = []
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/variables/variable'):
        if len(child.findall('./level-types/level-type')) == 1:
            if child.find('./level-types/level-type').attrib['type']=='soil-level' or child.find('./level-types/level-type').attrib['type']=='model-level':
                continue
            else:
                variables.append([child.attrib['name'], child.attrib['description']])    
        else:
            variables.append([child.attrib['name'], child.attrib['description']])
    # the user selects the description he wants with inquirer : he can have multiple variables 
    questions = [inquirer.Checkbox('description', message="select the variables: ", choices=[x[1] for x in variables])]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the variables
    description_variables = answers['description']

    # re associate the variables selected with the name in variables
    variables_selected = []
    for desc_var in description_variables:
        for variable in variables:
            if desc_var == variable[1]:
                variables_selected.append([variable[0], variable[1]])           

    # select the level type in class, model, level_types, level_type
    # return all the level types : key value (type, name) in a list
    for var in variables_selected:
        variable_type = []
        level_types_path = root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/variables/variable[@name="' + var[0] + '"]/level-types')
        for child in level_types_path.findall('./level-type'):
            if child.attrib['type']=='soil-level' or child.attrib['type']=='model-level':
                continue
            else:
                variable_type.append([child.attrib['type'], child.attrib['name']])
        # get all the possible key for variable_type : type
        types_ = list(set([x[0] for x in variable_type]))
        if len(types_) == 1:
            level_type = types_[0]
        else:
            # the user selects the level type he wants with inquirer : he can only select one level type 
            questions = [inquirer.List('level_type', message="select the level type for the variable " + var[0] + ' : ' + var[1], choices=types_)]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the level type
            level_type = answers['level_type']    
        
        # in variable_type, find all the level type names corresponding to the level type selected
        level_type_name = []
        for var_type in variable_type:
            if var_type[0] == level_type:
                level_type_name.append(var_type[1])
        level_type_names = list(set(level_type_name))
        if len(level_type_names) == 1:
            level_type_name = level_type_names[0]
        else:
            # the user selects the level type name he wants with inquirer : he can only have one level type name
            questions = [inquirer.List('level_type_name', message="select the level type name ", choices=level_type_name)]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the level type name
            level_type_name = answers['level_type_name']
        
        # if the level type is not single-level or time-invariant, the user needs to select the levels
        if level_type != 'single-level' and level_type != 'time-invariant':
            levels = []
            level_type_path = root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/variables/variable[@name="' + var[0] + '"]/level-types/level-type[@name="' + level_type_name + '"]')
            # present the corresponding levels to the user in class, model, levels, level_type, level_type_name
            for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/levels/' + level_type + '/' + level_type_name + '/level'):
                levels.append(child.attrib['value'])
        else:
            levels = None
        # append all the parameters in a dict : selected_variables
        dict = {'variable': var[0],'description':var[1] , 'level_type': level_type, 'level_type_name': level_type_name, 'levels': levels}
        list_variables.append(dict)
    selected_variables['variables'] = list_variables
    return selected_variables

def confirm_variables_NWP(selected_variables, data_name):
    # with rich console, print the variables selected
    console = Console()
    table = Table(title="Variables selected for "+ data_name)
    table.add_column("Variable")
    table.add_column("Description")
    table.add_column("Level type")
    table.add_column("Label")

    for variable in selected_variables['variables']:
        table.add_row(variable['variable'], variable['description'], variable['level_type'], variable['level_type_name'])

    console.print(table)
    # with inquirer, ask if the user wants to confirm the variables selected
    questions = [inquirer.Confirm('confirm', message="confirm the variables selected ?", default=True)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the answer
    confirm = answers['confirm']
    return confirm

################################################################
########################  LEVELS NWP  ##########################
################################################################

def get_levels(path_parameters, name_file):
    # go in the params_variables.json : path_parameters, name_file
    # get the selected variables
    with open(os.path.join(path_parameters, name_file)) as json_file:
        levels_by_types = {}
        # name of the model is the first key level in the json file
        data = json.load(json_file)
        # get the names of the models : key level 1
        model_names = list(data.keys())
        level_type_names = []
        for model_name in model_names:
            levels = []
            # list every variables : value of the key level 2
            variables = list(data[model_name]['variables'])
            #print(variables)
            #print(variables[0])
            for variable in variables:
                #print(variable.values())
                levels = variable['levels']
                if levels is not None:
                    levels = [int(i) for i in levels]
                    levels = sorted(levels)
                    type_name = variable['level_type_name']
                    # list every level_type_name : value of the key level 3
                    if type_name not in levels_by_types.keys():
                        levels_by_types[type_name] = levels
                    else:
                        common_levels =  levels_by_types[type_name]
                        common_levels = list(set.intersection(*map(set, [common_levels, levels])))
                        common_levels = sorted(common_levels)
                        levels_by_types[type_name] = common_levels 
        # with inquirer, ask for a list of levels for each type of level in levels_by_types
        questions = []
        for type_name in levels_by_types.keys():
            questions.append(inquirer.Checkbox(type_name, message="select the levels for the type " + type_name, choices=levels_by_types[type_name]))
            # get the answer
            answers = inquirer.prompt(questions)
            # get the levels
            levels = answers[type_name]
            levels_by_types[type_name] = levels
        
        for model_name in model_names:
            variables = list(data[model_name]['variables'])
            for variable in variables:
                for type_name in levels_by_types.keys():
                    if variable['level_type_name'] == type_name:
                        #variable['levels'] = levels_by_types[type_name]
                        data[model_name]['variables'][variables.index(variable)]['levels'] = levels_by_types[type_name]
    

    return levels_by_types, data

def confirm_levels_NWP(levels):
    # with rich console, print the levels selected
    console = Console()
    table = Table(title="Levels selected")
    table.add_column("Level Label")
    table.add_column("Level(s)")
    for level_type in levels.keys():
        for level in levels[level_type]:
            table.add_row(level_type, str(level))
    console.print(table)
    # with inquirer, ask if the user wants to confirm the levels selected
    questions = [inquirer.Confirm('confirm', message="confirm the levels selected ?", default=True)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the answer
    confirm = answers['confirm']
    return confirm


################################################################
###########################  UTILS  ############################
################################################################

def get_config_paths(path):
    # get the root of the xml file<
    tree = ET.parse(path)
    root = tree.getroot()
    # find the class name above the root
    class_name = root.find('./class').attrib['name']
    # find the model name
    model_name = root.find('./class[@name="' + class_name + '"]/model').attrib['name']
    return root, class_name, model_name

################################################################
###################### RUN AVAILABILITY ########################
################################################################

def runs_available(conf_path, class_name, model_name):
    # open the xml file
    tree = ET.parse(conf_path)
    # get the root of the xml file
    root = tree.getroot()
    # get the number of days available in the xml file
    nb_days = int(root.find('./class[@name="' + class_name + '"]/days_storage').attrib['value'])
    # create a tab with the days depending on nb days
    days = []
    for i in range(0, nb_days+1):
        days.append(datetime.date.today() - datetime.timedelta(days=i))
    # find all the run hours available
    runs = []
    # in class name, in model, in run_hours, get the 'hour' attribute
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/run_hours'):
        # print the hour
        runs.append(child.attrib['hour'])
    #get the delivery hours
    delivery_hours = []
    delivered_next_day = []
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/run_hours'):
        delivery_hours.append(child.attrib['delivery_hour'])
        delivered_next_day.append(child.attrib['next_day'])
    #with days and delivery hours, create a tab with all the delivery times with format YYYYMMDDHH
    run_times = []
    delivery_times = []
    for day in days:
        for run_hour, deliv_hour, next_day in zip(runs ,delivery_hours, delivered_next_day):
            run_times.append(datetime.datetime.strptime(day.strftime("%Y-%m-%d") + " " + run_hour.zfill(2) + ":00:00", "%Y-%m-%d %H:%M:%S"))
            if next_day == "True":
                day = day + datetime.timedelta(days=1)
            # format it in datetime.datetime YYYY-MM-DD HH:00:00
            delivery_times.append(datetime.datetime.strptime(day.strftime("%Y-%m-%d") + " " + deliv_hour.zfill(2) + ":00:00", "%Y-%m-%d %H:%M:%S"))
    #if the delivery time is superior to now, remove it from the list
    #if the delivery is limited last day, remove the hours inferior to now
    now = datetime.datetime.now()
    # place a delta of 1 hour to be sure to remove the run if the delivery is in the next hour and the run is not available anymore
    # place a delta of 1 hour to be sure to add the run when the run is available 
    delta = datetime.timedelta(hours=2)
    removed_runs = []
    for run, deliv_time in zip(run_times, delivery_times):
        # if the delivery is superior to now, remove the run
        if deliv_time > now - delta:
            removed_runs.append(run)
        # if the delivery is limited last day, remove the hours inferior to now nb_days ago
        limit_last_day = str(root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/limit_last_day').attrib['value'])
        if limit_last_day == "False": limit_last_day = False
        else: limit_last_day = True
        if limit_last_day and deliv_time < now + delta - datetime.timedelta(days=nb_days):
            removed_runs.append(run)
    # remove the runs from the list
    for run in removed_runs:
        run_times.remove(run)
    # extract the days from the runs available
    run_days = []
    for run in run_times:
        run_days.append(run.date())
    # return the runs available
    return run_times, run_days

def get_Runs_Each_Day(conf_path, class_name, model_name, day):
    # for a selected day, get the runs available
    # call function available_runs and get the runs available for the selected day
    available_runs, available_days = runs_available(conf_path, class_name, model_name)
    runs = []
    for run in available_runs:
        # extract the day from the run in available_runs which is a datetime.datetime object
        if run.date() == day:
            # append the run in the list, format run in string : HH
            runs.append(str(run.hour).zfill(2))
    return runs 

def get_Common_Days(list_paths):
    available_runs = []
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path) 
        # call the function runs_available to get the runs available and the days available
        available_runs_source, available_days_source = runs_available(path, class_name, model_name)
        available_runs.append(available_runs_source)
    # get all the common runs between the sources
    list_common_runs = list(set.intersection(*map(set, available_runs)))
    # extract the days from the runs available
    common_days = []
    for run in list_common_runs:
        common_days.append(run.date())
    # list the days uniquely
    common_days = list(set(common_days))
    # return the common days
    return common_days

def get_Common_Runs(list_paths, day):
    runs = []
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path)
        # call the function get_Runs_Each_Day to get the runs available for the selected day
        available_runs_source = get_Runs_Each_Day(path, class_name, model_name, day)
        runs.append(available_runs_source)
    runs = list(set.intersection(*map(set, runs)))
    return runs

def select_day_and_run(list_paths):
    # with inquirer ask if the user wants to select a specific day and run or last available
    questions = [inquirer.List('option', message="select the option: ", choices=['last available', 'specific day and run'])]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the option
    option = answers['option']
    # if the option is last available, get the last available day and run
    if option == 'last available':
        common_days = get_Common_Days(list_paths)
        if not common_days:
            print('no common days between the sources')
            return None, None
        else:
            # last day is the latest frome the common days : analyse the days in datetime.date format
            last_day = common_days[0]
            for day in common_days:
                if day > last_day:
                    last_day = day
            common_runs = get_Common_Runs(list_paths, last_day)
            # last run is the latest from the common runs : analyse the runs in string format
            last_run = int(common_runs[0])
            for run in common_runs:
                if int(run) > last_run:
                    last_run = int(run)
            print('last available day : ', last_day, ' last available run : ', last_run,' h')
            day = last_day.strftime("%Y%m%d")
            # last run is int : format it in string : HH
            run = str(last_run).zfill(2)
    else:
        common_days = get_Common_Days(list_paths)
        # if common days is empty : no common days between the sources
        if not common_days:
            print('no common days between those sources')
            return None, None
        else:
            # with inquirer, ask for a day with the list of the available days
            questions = [inquirer.List('day', message="select the day: ", choices=common_days)]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the day
            day = answers['day']
            common_runs = get_Common_Runs(list_paths, day)
            # with inquirer, ask for a run with the list of the available runs
            questions = [inquirer.List('run', message="select the hours of the run : ", choices=common_runs)]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the run
            run = answers['run']
            # format day and run to YYYYMMDDHH
            day = day.strftime("%Y%m%d")
            run = run.zfill(2)
            date = day + run
    return day, run

################################################################
####################  FORECAST REGRIDING  ######################  
################################################################

def list_forecasts(conf_path, class_name, model_name,run):
    root = ET.parse(conf_path).getroot()
    # go in class, model, run_hours, Hours_Steps, 
    fc_step_hours = []
    # in class name run, in model, in run_hours, Hours_Steps, get the steps with attribute 'hour'
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/run_hours[@hour="' + run + '"]/Hours_Steps/step'):
        # print the steps
        fc_step_hours.append(child.attrib['hours'])
    fc_hours = []
    for fc_step_hour in fc_step_hours:
        # retrieve lower and higher limit of the forecast hours available
        min, max = 0, 0
        for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]//run_hours[@hour="' + run + '"]/Hours_Steps/step[@hours="' + fc_step_hour + '"]'):
            # print the steps
            min = child.attrib['min']
            max = child.attrib['max']
        for i in range(int(min), int(max) + 1, int(fc_step_hour)):
            fc_hours.append(i)
    return fc_hours

def get_timesteps(common_hours):
    dict_timesteps = {1, 3, 6}
    # get maximum value of the common hours
    max = 0
    for hour in common_hours:
        if hour > max:
            max = hour

    hourly = []
    # for hourly forecast : add all the hours while it can be added 1 by 1
    for hour in range(0, max+1):
        if hour in common_hours:
            hourly.append(hour)
        else:
            break
    
    three_hourly = []
    # for three hourly forecast : add all the hours while it can be added 3 by 3
    for hour in range(0, max+1, 3):
        if hour in common_hours:
            three_hourly.append(hour)
        else:
            break
        
    six_hourly = []
    # for six hourly forecast : add all the hours while it can be added 6 by 6
    for hour in range(0, max+1, 6):
        if hour in common_hours:
            six_hourly.append(hour)
        else:
            break

    return hourly, three_hourly, six_hourly

def temporal_interpolation(fc_hours):
    # if the option is temporal interpolation, get the forecast hours available 
    maxes = []
    for fc_hours_source in fc_hours:
        # get the maximum value of the forecast hours available
        max = 0
        for hour in fc_hours_source:
            if hour > max:
                max = hour
        maxes.append(max)
    # get the minimum value of the maximum values
    min = 1000
    for hour in maxes:
        if hour < min:
            min = hour
    interpolated_hours = []
    for i in range(0, min+1):
        interpolated_hours.append(i)
    return interpolated_hours

def select_common_forecast(list_paths, run):
    # create a list with all the forecast hours available for the run hour selected for each model
    fc_hours = []
    dict_forecast_hours = {}
    for path in list_paths:
        # get config paths
        root, class_name, model_name = get_config_paths(path)
        # get all the forecast hours available for the run hour selected
        fc_hours_source = list_forecasts(path, class_name, model_name, run)
        fc_hours.append(fc_hours_source)
        dict_forecast_hours[class_name] = fc_hours_source
    # get all the common forecast hours between the sources
    common_fc_hours = list(set.intersection(*map(set, fc_hours)))
    # get the timesteps for each type of temporal interpolation
    hourly, three_hourly, six_hourly = get_timesteps(common_fc_hours)
    # with inquirer, ask for an option : hourly, three hourly, six hourly
    questions = [inquirer.List('option', message="select the option: ", choices=['hourly', 'three hourly', 'six hourly', 'temporal interpolation'])]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the option
    option = answers['option']
    # if the option is hourly, with inquirer ask for a list of the forecast hours available hourly
    if option == 'hourly':
        questions = [inquirer.Checkbox('hour', message="select the forecast hours: ", choices=hourly)]
        # get the answer
        answers = inquirer.prompt(questions)
        # get the forecast hours
        fc_hours = answers['hour']
    # if the option is three hourly, with inquirer ask for a list of the forecast hours available three hourly
    elif option == 'three hourly':
        questions = [inquirer.Checkbox('hour', message="select the forecast hours: ", choices=three_hourly)]
        # get the answer
        answers = inquirer.prompt(questions)
        # get the forecast hours
        fc_hours = answers['hour']
    # if the option is six hourly, with inquirer ask for a list of the forecast hours available six hourly
    elif option == 'six hourly':
        questions = [inquirer.Checkbox('hour', message="select the forecast hours: ", choices=six_hourly)]
        # get the answer
        answers = inquirer.prompt(questions)
        # get the forecast hours
        fc_hours = answers['hour']
    elif option == 'temporal interpolation':
        fc_hours = temporal_interpolation(fc_hours)
        # with inquirer, ask for a list of the forecast hours available hourly
        questions = [inquirer.Checkbox('hour', message="select the forecast hours: ", choices=fc_hours)]
        # get the answer
        answers = inquirer.prompt(questions)
        # get the forecast hours
        fc_hours = answers['hour']
    return fc_hours, option, dict_forecast_hours

def confirm_forecast(selected_observations):
    # with rich console, print the forecast hours selected : {'run_time': run_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), 'forecast_time': forecast_time}
    console = Console()
    table = Table(title="Forecast hours selected")
    table.add_column("run_time")
    table.add_column("forecasts")
    run_time = selected_observations['run_time']
    for forecast_time in selected_observations['forecasts']:
        table.add_row(run_time, forecast_time)
    console.print(table)
    # with inquirer, ask if the user wants to confirm the forecast hours selected
    questions = [inquirer.Confirm('confirm', message="confirm the forecast hours selected ?", default=True)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the answer
    confirm = answers['confirm']
    return confirm


################################################################
########################  SELECT INTERPOLATION  ################
################################################################

def select_grid_interpolation():
    # with inquirer ask which grid the user wants to interpolate the data to
    # ask the user to select the grid between 0.5 and 0.01
    questions = [
        inquirer.Text('grid', message="select the grid between 0.5 and 0.01 ")
    ]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the grid
    grid = answers['grid']
    # if the grid is not a float and not in range 0.01, 0.5, ask again
    while True:
        try:
            if (float(grid) < 0.01 or float(grid) > 0.5):
                raise ValueError
            break
        except:
            questions = [
                inquirer.Text('grid', message="select the grid between 0.5 and 0.01 ")
            ]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the grid
            grid = answers['grid']
    grid = float(grid)
    return grid
    
# select lat lon box
def select_box():
    questions = [inquirer.Text('lon', message="select the western longitude between -180 and 180")]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the latitude
    western_lon = answers['lon']
    # western_lonitude
    while True:
        try:
            # if lat is not a float and not in range -90, 90, ask again
            if (float(western_lon) < -180 or float(western_lon) > 180):
                raise ValueError
            break
        except:
            questions = [inquirer.Text('lon', message="select the western longitude between -180 and 180 ")]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the latitude
            western_lon = answers['lon']
    western_lon = float(western_lon)
    # eastern_lonitude
    while True:
        try:
            # if lat is not a float and not in range western_lon, 90, ask again
            if (float(eastern_lon) < western_lon or float(eastern_lon) > 180):
                raise ValueError
            break
        except:
            questions = [inquirer.Text('lon', message="select the eastern longitude between " + str(western_lon) + " and 180 ")]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the latitude
            eastern_lon = answers['lon']
    eastern_lon = float(eastern_lon)
    # southern_latgitude
    while True:
        try:
            # if lon is not a float and not in range -180, 180, ask again
            if (float(southern_lat) < -90 or float(southern_lat) > 90):
                raise ValueError
            break
        except:
            questions = [inquirer.Text('lat', message="select the southern latitude between -90 and 90 ")]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the longitude
            southern_lat = answers['lat']
    southern_lat = float(southern_lat)
    # northern_latgitude
    while True:
        try:
            # if lon is not a float and not in range southern_lat, 180, ask again
            if (float(northern_lat) < southern_lat or float(northern_lat) > 90):
                raise ValueError
            break
        except:
            questions = [inquirer.Text('lat', message="select the northern latitude between " + str(southern_lat) + " and 90")]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the longitude
            northern_lat = answers['lat']
    northern_lat = float(northern_lat)
    return str(western_lon), str(eastern_lon), str(southern_lat), str(northern_lat)
