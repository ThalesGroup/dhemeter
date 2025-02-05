import lxml.etree as ET
import os
import datetime
import requests
import subprocess
import calendar
import inquirer
from rich.console import Console
from rich.table import Table

################################################################
########################  VARIABLES NWP  #######################
################################################################

def select_variables_REA(REA_path):
    selected_variables= {}
    
    root, class_name, model_name = get_config_paths(REA_path)

    # select the variable in class, model, variables, variable
    # variables takes key value (name, description)
    variables = []
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/variables/variable'):
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
            variable_type.append([child.attrib['type'], child.attrib['name']])
        # get all the possible key for variable_type : type
        types_ = list(set([x[0] for x in variable_type]))
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
            # and if the variable has min or max attributes : means we have a range of levels : calculate the levels between min and max
            min, max = 0, 0
            if 'min' in level_type_path.attrib and 'max' in level_type_path.attrib:
                min = int(child.attrib['min'])
                max = int(child.attrib['max'])
                print('between ', min, ' and ', max)
                for i in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/levels/' + level_type + '/' + level_type_name + '/level'):
                    if int(i.attrib['value']) >= min and int(i.attrib['value']) <= max:
                        levels.append(i.attrib['value'])
            else:
                # present the corresponding levels to the user in class, model, levels, level_type, level_type_name
                for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/levels/' + level_type + '/' + level_type_name + '/level'):
                    levels.append(child.attrib['value'])
            # the user selects the level he wants with inquirer : he can have multiple levels
            questions = [inquirer.Checkbox('levels', message="select the levels ", choices=levels)]
            # get the answer
            answers = inquirer.prompt(questions)
            # get the levels
            levels = answers['levels']
        else:
            levels = None
        # append all the parameters in a dict : selected_variables
        selected_variables[var[0]] = {'level_type': level_type, 'level_type_name': level_type_name, 'levels': levels}
        
    return selected_variables
    

################################################################
###########################  UTILS  ############################
################################################################

def get_config_paths(path):
    # get the root of the xml file
    tree = ET.parse(path)
    root = tree.getroot()
    # find the class name above the root
    class_name = root.find('./class').attrib['name']
    # find the model name
    model_name = root.find('./class[@name="' + class_name + '"]/model').attrib['name']
    return root, class_name, model_name

################################################################
#################### OBS/RUN AVAILABILITY ######################
################################################################
def select_time_obs(list_paths, date_):
    days = []
    for path in list_paths:
        days_model = []
        root, class_name, model_name = get_config_paths(path)
        # open the xml file
        tree = ET.parse(path)
        # get the root of the xml file
        root = tree.getroot()
        # retrieve the root of the request data
        nb_days = int(root.find('./class[@name="' + class_name + '"]/days_storage').attrib['value'])
        # elapsed days is the diff between the date_ and today
        elapsed_days = (datetime.datetime.now() - date_).days
        nb_days = nb_days - elapsed_days
        # create a list of the days available between the last day and now
        for i in range(0, nb_days):
            days_model.append((date_ - datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
        days.append(days_model)
    # select the days in common between the requests
    days = list(set(days[0]).intersection(*days))
    # Now we have the list of all the common days available for all the requests
    # order the days in the list from the most recent to the oldest
    days.sort(reverse=True)
    # with inquirer, ask for a day with the list of the available days
    questions = [inquirer.List('day', message="select the day: ", choices=days)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the day
    day = datetime.datetime.strptime(answers['day'], "%Y-%m-%d")
    # create a list of the hours available between 00-00 and 23-59 depending on the day selected
    hours = []
    for i in range(0, 24):
        if day.date() == date_.date() and i > date_.hour:
            break
        else:
            hours.append(str(i))
    # with inquirer, ask for a hour with the list of the available hours
    questions = [inquirer.List('hour', message="select the hour of the observation: ", choices=hours)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the hour
    hour = datetime.datetime.strptime(answers['hour'], "%H")
    # concatenate the day and the hour in a format : YYYY-MM-DD-HH
    day = day.strftime("%Y-%m-%d") + '-' + hour.strftime("%H")
    day = datetime.datetime.strptime(day, "%Y-%m-%d-%H")
    # create a list of the minutes available between 00 and 59
    minutes = []
    for i in range(0, 60):
        # if the day is today, get the minutes available depending on the hour selected
        if day.date() == date_.date() and day.hour == date_.hour and i > date_.minute: 
            break
        else:
            minutes.append(str(i))
    # with inquirer, ask for a minute with the list of the available minutes
    questions = [inquirer.List('minute', message="select the minute of the observation: ", choices=minutes)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the minute
    minute = datetime.datetime.strptime(answers['minute'], "%M")
    # concatenate the day, the hour and the minute in a format : YYYY-MM-DD-HH-MM
    day = day.strftime("%Y-%m-%d-%H") + '-' + minute.strftime("%M")
    day = datetime.datetime.strptime(day, "%Y-%m-%d-%H-%M")
    return day

# defines a couple of start and end time for the request
def select_free_range_obs(list_paths):
    delay = 0
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path)
        # open the xml file
        tree = ET.parse(path)
        # get the root of the xml file
        root = tree.getroot()
        # retrieve the root of the request data
        delay_path = int(root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/delay').attrib['value'])
        if delay_path > delay:
            delay = delay_path
    now = datetime.datetime.now()
    delayed_now = now - datetime.timedelta(days=int(delay))
    if delayed_now.day != now.day:
        # set delayed now to 23:00:00
        delayed_now = datetime.datetime.strptime(delayed_now.strftime("%Y-%m-%d") + " 23:00:00", "%Y-%m-%d %H:%M:%S")

    print("########## START TIME #########")
    start_time = select_time_obs(list_paths, delayed_now)
    print("########### END TIME #########")
    end_time = select_time_obs(list_paths, start_time)
    return start_time, end_time

def list_time_obs(list_paths):
    hours = []
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path)
        # open the xml file
        tree = ET.parse(path)
        # get the root of the xml file
        root = tree.getroot()
        # if type_observation = past-hours, list all the hours available
        hours_model = []
        if root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/type_observation').attrib['value'] == 'past-hours':
            for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/past-hours/hour'):
                hours_model.append(child.attrib['value'])
            hours.append(hours_model)
    # select the hours in common between the requests
    hours = list(set(hours[0]).intersection(*hours))
    # Now we have the list of all the common hours available for all the requests
    return hours

def select_range_obs(list_paths):
    Now = datetime.datetime.now()
    start_time = select_time_obs(list_paths, Now)
    list_end = list_time_obs(list_paths)
    # with inquirer, ask for a hour with the list of the available hours
    questions = [inquirer.List('hour', message="select how many hours you need to observe: ", choices=list_end)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the hour
    hour = int(answers['hour'])
    # substraction of the hour selected to the start time
    end_time = start_time - datetime.timedelta(hours=hour)
    return start_time, end_time

def run_obs_available(conf_path, class_name, model_name, start_time, end_time):
    now = datetime.datetime.now()
    # open the xml file
    tree = ET.parse(conf_path)
    # get the root of the xml file
    root = tree.getroot()
    # create a tab with the days depending on start time and end time
    days = []
    # START TIME : 2023-09-05 00:00:00 END TIME : 2023-09-03 22:00:00
    # round start time and end time to 00:00:00
    start_time_round = datetime.datetime.strptime(start_time.strftime("%Y-%m-%d") + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_time_round = datetime.datetime.strptime(end_time.strftime("%Y-%m-%d") + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    nb_days = (start_time_round - end_time_round).days + 1 # +1 because we need to include the end day
    for i in range(0, nb_days):
        days.append(start_time - datetime.timedelta(days=i))
    
    # find all the run hours available
    runs = []
    #get the delivery hours
    delivery_hours = []
    delivered_next_day = []
    for child in root.findall('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/obs-hours'):
        delivery_hours.append(child.attrib['delivery_hour'])
        delivered_next_day.append(child.attrib['next_day'])
        runs.append(child.attrib['hour'])
    #with days and delivery hours, create a tab with all the delivery times with format YYYYMMDDHH
    run_times = []
    delivery_times = []
    for day in days:
        for run_hour, deliv_hour, next_day in zip(runs ,delivery_hours, delivered_next_day):
            # format it in datetime.datetime YYYY-MM-DD HH : with the run hour
            run_times.append(datetime.datetime.strptime(day.strftime("%Y-%m-%d") + " " + run_hour.zfill(2) + ":00:00", "%Y-%m-%d %H:%M:%S"))
            if next_day == "True":
                deliv_day = day + datetime.timedelta(days=1)
                # format it in datetime.datetime YYYY-MM-DD HH:00:00
            else:
                deliv_day = day
            delivery_times.append(datetime.datetime.strptime(deliv_day.strftime("%Y-%m-%d") + " " + deliv_hour.zfill(2) + ":00:00", "%Y-%m-%d %H:%M:%S"))
    removed_runs = []
    for run, deliv_time in zip(run_times, delivery_times):
        # if the obs is superior to start_time, remove the obs
        if run > start_time:
            removed_runs.append(run)
        # if the obs hour is inferior to end_time, remove the obs
        elif run < end_time:
            removed_runs.append(run)
        # if the delivery is superior to now, remove the obs
        elif deliv_time > now:
            removed_runs.append(run)
        # if the delivery is limited last day, remove the hours inferior to start_time nb_days ago
        limit_last_day = str(root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/limit_last_day').attrib['value'])
        if limit_last_day == "False": limit_last_day = False
        else: limit_last_day = True
        if limit_last_day and deliv_time < now - datetime.timedelta(days=nb_days) :
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

# in the ranges of hours : find all the possible "obs hours" for the list of paths
def list_run_obs(list_paths, start_time, end_time):
    dict_obs = {}
    # convert start_time and end_time in Str YYYYMMDDHHMM
    dict_obs['start_time'] = start_time.strftime("%Y%m%d%H%M")
    dict_obs['end_time'] = end_time.strftime("%Y%m%d%H%M")
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path)
        # open the xml file
        tree = ET.parse(path)
        # get the root of the xml file
        root = tree.getroot()
        # if type_observation = obs-hours, list all the hours available
        obs_hours = []
        run_obs = []
        
        if root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/type_observation').attrib['value'] == 'obs-hours':
            list_obs, list_days = run_obs_available(path, class_name, model_name, start_time, end_time)
            # dict_obs : key = path, value = list_obs : append the list of obs hours for each path and append the dict_obs
            # with update method : dict_obs.update({path: list_obs})
            for obs in list_obs:
                obs_hours.append(obs.strftime("%Y%m%d%H%M"))
            dict_obs.update({path: obs_hours})
    return dict_obs

def global_rea_selection(list_paths):
    obs_types = []
    for path in list_paths:
        root, class_name, model_name = get_config_paths(path)
        # check the type of observation
        type_observation = root.find('./class[@name="' + class_name + '"]/model[@name="' + model_name + '"]/type_observation').attrib['value']
        obs_types.append(type_observation)
    # If obs_types contains only free-range, select_free_range_obs
    if obs_types.count('free-range') == len(obs_types):
        start_time, end_time = select_free_range_obs(list_paths)
        return list_run_obs(list_paths, start_time, end_time)
    # if obs_types contains only obs-hours, select_free_range_obs
    if obs_types.count('obs-hours') == len(obs_types):
        start_time, end_time = select_free_range_obs(list_paths)
        return list_run_obs(list_paths, start_time, end_time)
    # if obs_types contains only past-hours, select_range_obs
    elif obs_types.count('past-hours') == len(obs_types):
        start_time, end_time = select_range_obs(list_paths)
        return list_run_obs(list_paths, start_time, end_time)
    # if obs_types contains both obs-hours and past-hours, select range obs then list run obs
    else:
        start_time, end_time = select_range_obs(list_paths)
        return list_run_obs(list_paths, start_time, end_time)


def confirm_observation(selected_observations):
    # with rich console, print the forecast hours selected
    console = Console()
    table = Table(title="Observation hours selected")
    # {"reanalysis_time": ["2024-07-18T00:00:00.000Z", "2024-07-18T01:00:00.000Z", "2024-07-18T02:00:00.000Z", "2024-07-18T03:00:00.000Z", "2024-07-18T04:00:00.000Z", "2024-07-18T05:00:00.000Z", "2024-07-18T06:00:00.000Z"]}
    table.add_column("Observation hours")
    for obs in selected_observations['reanalysis_time']:
        table.add_row(obs)
    console.print(table)
    # with inquirer, ask if the user wants to confirm the forecast hours selected
    questions = [inquirer.Confirm('confirm', message="confirm the observation hours selected ?", default=True)]
    # get the answer
    answers = inquirer.prompt(questions)
    # get the answer
    confirm = answers['confirm']
    return confirm

