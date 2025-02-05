import lxml.etree as ET
import os
import datetime
import requests
import subprocess
import calendar
import ICAO, IGRA, MF
import inquirer
import json


################################################################
########################  NB REQUESTS  #########################
################################################################

def select_nb_requests(source_name):
    if source_name == 'NWP':
        # the user is limited to 2 requests
        # with inquirer choose the number of requests
        questions = [
            inquirer.List('nb_request', message="how many sources needs to be agregated? ", choices=['1', '2', '3'])]
    if source_name == 'OBS':
        # the user is limited to 10 requests
        # with inquirer choose the number of requests
        questions = [inquirer.List('nb_request', message="how many sources needs to be agregated? ",
                                   choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])]
    if source_name == 'REANALYSIS' or source_name == 'SAT':
        # the user is limited to 2 requests
        # with inquirer choose the number of requests
        questions = [
            inquirer.List('nb_request', message="how many sources needs to be agregated? ", choices=['1', '2'])]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the nb_request
    nb_request = answers['nb_request']
    #  convert the input to an integer
    nb_request = int(nb_request)
    #  return the nb_request
    return nb_request


################################################################
#######################  SELECT SOURCE  ########################
################################################################

def select_source():
    #  find all the type MODELS in the xml file
    #  get the root of the xml file
    root = os.path.join(os.getcwd(), 'MODELS.xml')
    #  open the xml file
    tree = ET.parse(root)
    # find all the SOURCES in the xml file
    sources = tree.findall('./SOURCES/*')
    sources_name = []
    # print the name of the sources
    for source in sources:
        # add the name of the source in a list
        sources_name.append(source.tag)
    # with inquirer, present the list of the sources and ask to select one
    questions = [inquirer.List('source_name', message="select the type of data ", choices=sources_name)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the source name
    source_name = answers['source_name']
    #  find all the MODEL in the type (NWP, AIR, SOL, SAT) in the xml file
    models = tree.findall('./SOURCES/' + source_name + '/MODEL')
    models_name = []
    for model in models:
        # add the name of the model in a list
        models_name.append(model.attrib['name'])
    #  with inquirer, ask to select one
    questions = [inquirer.List('model_name', message="select the model or source ", choices=models_name)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the model name
    model_name = answers['model_name']
    #  find the model in the xml file and get the path
    model = tree.find('./SOURCES/' + source_name + '/MODEL[@name="' + model_name + '"]')
    #  get the path of the model and string it
    model_path = model.attrib['path']
    return model_path, model_name


################################################################
#######################  SELECT KIND  ########################
################################################################

def select_kind(workdir):
    #  find all the type MODELS in the xml file
    #  get the root of the xml file
    root = os.path.join(workdir, 'MODELS.xml')
    #  open the xml file
    tree = ET.parse(root)
    # find all the SOURCES in the xml file
    sources = tree.findall('./SOURCES/*')
    sources_name = []
    # print the name of the sources
    for source in sources:
        # add the name of the source in a list
        sources_name.append(source.tag)

    # with inquirer, present the list of the sources and ask to select one
    questions = [inquirer.List('source_name', message="select the type of data ", choices=sources_name)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the source name
    source_name = answers['source_name']

    metaparams_types = tree.findall('./SOURCES/' + source_name + '/*')
    dict_params = {}
    for metaparam_type in metaparams_types:
        list_params = []
        metaparams = tree.findall('./SOURCES/' + source_name + '/' + metaparam_type.tag)
        for metaparam in metaparams:
            list_params.append(metaparam.attrib['name'])
        dict_params[metaparam_type.tag] = list_params

    #  catch in the source_name tag : get the name of the workflow template : ./SOURCES/source_name attrib workflow-name
    workflow_name = tree.find('./SOURCES/' + source_name).attrib['workflow-name']

    return dict_params, source_name, workflow_name


def get_available_sources(source_name, workdir):
    #  find all the type MODELS in the xml file
    #  get the root of the xml file
    root = os.path.join(workdir, 'MODELS.xml')
    #  open the xml file
    tree = ET.parse(root)
    #  find all the MODEL in the type (NWP, AIR, SOL, SAT) in the xml file
    models = tree.findall('./SOURCES/' + source_name + '/MODEL')
    models_name = []
    models_path = []
    for model in models:
        # add the name of the model in a list
        models_name.append(model.attrib['name'])
        models_path.append(model.attrib['path'])
    return models_name, models_path


################################################################
######################## SELECT DATA ###########################
############################################################### 

def select_data(source_name, available_sources, workdir):
    #  find all the type MODELS in the xml file
    #  get the root of the xml file
    root = os.path.join(workdir, 'MODELS.xml')
    #  open the xml file
    tree = ET.parse(root)
    #  find all the MODEL in the type (NWP, AIR, SOL, SAT) in the xml file
    all_models = tree.findall('./SOURCES/' + source_name + '/MODEL')
    models_name = []
    for model in all_models:
        # apppend the ones that are in available_sources
        if model.attrib['name'] in available_sources:
            models_name.append(model.attrib['name'])
    #  with inquirer, ask to select one
    questions = [inquirer.List('model_name', message="select the model or source ", choices=models_name)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the model name
    model_name = answers['model_name']
    #  find the model in the xml file and get the path
    model = tree.find('./SOURCES/' + source_name + '/MODEL[@name="' + model_name + '"]')
    #  get the path of the model and string it
    model_path = model.attrib['path']
    conf_path = os.path.join(model_path, 'conf.xml')
    return model_path, model_name, conf_path


################################################################
########################  WRITE json  ###########################
################################################################
#  write the json file according to the selected variables
def write_json_air(data_path, parameters, name_file, append=None):
    param_file_name = name_file
    #  if the file exists, append the new variables
    if append is not None:
        #  if the file doesn't exist, create it
        if not os.path.exists(os.path.join(data_path, param_file_name)):
            json_obj = []
        #  append is an index for putting an index as a key in the json file
        else:
            with open(os.path.join(data_path, param_file_name), 'r') as f:
                json_obj = json.load(f)
        #  append the new variables
        # even if append tag exist in the json file, do not overwrite it, create a new append tag
        dict_ = {append: parameters}
        json_obj.append(dict_)
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)
    #  if the file doesn't exist, create it
    else:
        json_obj = {}
        json_obj = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)


def write_json_nwp(data_path, parameters, name_file, append=None):
    #  with json dump the selected variables in the json file
    param_file_name = name_file

    #  if the file exists, append the new variables
    if append is not None:
        #  if the file doesn't exist, create it
        if not os.path.exists(os.path.join(data_path, param_file_name)):
            json_obj = {}
        #  append is an index for putting an index as a key in the json file
        else:
            with open(os.path.join(data_path, param_file_name), 'r') as f:
                json_obj = json.load(f)
        #  append the new variables
        json_obj[append] = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)
    #  if the file doesn't exist, create it
    else:
        json_obj = {}
        json_obj = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)


def write_json_rea(data_path, parameters, name_file, append=None):
    #  with json dump the selected variables in the json file
    param_file_name = name_file

    #  if the file exists, append the new variables
    if append is not None:
        #  if the file doesn't exist, create it
        if not os.path.exists(os.path.join(data_path, param_file_name)):
            json_obj = {}
        #  append is an index for putting an index as a key in the json file
        else:
            with open(os.path.join(data_path, param_file_name), 'r') as f:
                json_obj = json.load(f)
        #  append the new variables
        json_obj[append] = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)
    #  if the file doesn't exist, create it
    else:
        json_obj = {}
        json_obj = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)


def write_json(data_path, parameters, name_file, append=None):
    #  with json dump the selected variables in the json file
    param_file_name = name_file

    #  if the file exists, append the new variables
    if append is not None:
        #  if the file doesn't exist, create it
        if not os.path.exists(os.path.join(data_path, param_file_name)):
            json_obj = {}
        #  append is an index for putting an index as a key in the json file
        else:
            with open(os.path.join(data_path, param_file_name), 'r') as f:
                json_obj = json.load(f)
        #  append the new variables
        json_obj[append] = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)
    #  if the file doesn't exist, create it
    else:
        json_obj = {}
        json_obj = parameters
        #  write the json file
        with open(os.path.join(data_path, param_file_name), 'w') as outfile:
            json_obj = json.dump(json_obj, outfile, indent=4)


################################################################
######################  CONTINUE OPTION  #######################
################################################################
def ask_request():
    # with inquirer, ask the question
    questions = [inquirer.Confirm('continue', message="Do you want to aggregate the selected data ? ", default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


def ask_merge():
    # with inquirer, ask the question
    questions = [inquirer.Confirm('continue', message="Do you want to aggregate the selected data ? ", default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


def ask_temporal_interp():
    # with inquirer, ask the question
    questions = [
        inquirer.Confirm('continue', message="Do you want to start the temporal interpolation process ?", default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


def ask_spatial_interp():
    # with inquirer, ask the question
    questions = [inquirer.Confirm('continue', message="Do you want to interpolate spatially ? ", default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


# ask if the user wants to continue or not
def ask_Remap_ICON_GLOBAL():
    # with inquirer, ask the question
    questions = [inquirer.Confirm('continue', message="ICON_GLOBAL files detected, Remap them or stop the process ",
                                  default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


def ask_box_lat_lon():
    # with inquirer, ask the question
    questions = [inquirer.Confirm('continue', message="Do you want to define a lat lon box ? ", default=True)]
    #  get the answer
    answers = inquirer.prompt(questions)
    #  get the continue
    continue_ = answers['continue']
    #  return the continue
    return continue_


################################################################
######################  METAPARAMETERS  ########################
################################################################
#  create a json with keys IFS, GFS, ICON-GLOBAL, ICON-EU, MERGE, interpolate-spatially, interpolate-temporally, grid, box, western_lon, eastern_lon, southern_lat, northern_lat
def create_metaparams(dict_params, source_name, metaparams_json, workdir):
    # the first key is the source name
    # TODO : Correction metadata.json
    # Before :
    """
    json_obj = {}
    json_obj[source_name] = {}
    # the second level of keys are the first level of the dict_params
    for key in dict_params.keys():
        json_obj[source_name][key] = {}
        for param in dict_params[key]:
            json_obj[source_name][key][param] = False
    """
    # Now :
    json_obj = {'SOURCE': source_name}
    for key in dict_params.keys():
        json_obj[key] = {}
        for param in dict_params[key]:
            json_obj[key][param] = False
    #  write the json file
    with open(os.path.join(workdir, metaparams_json), 'w') as outfile:
        json_ = json.dump(json_obj, outfile, indent=4)
    return json_obj


def set_metaparam(json_obj, source_name, type, param, value):
    # TODO : Correction metadata.json
    """
    json_obj[source_name][type][param] = value
    """
    json_obj[type][param] = value
    return json_obj


def dump_metaparams(json_obj, metaparams_json, params_path):
    with open(os.path.join(params_path, metaparams_json), 'w') as outfile:
        json_obj = json.dump(json_obj, outfile, indent=4)
