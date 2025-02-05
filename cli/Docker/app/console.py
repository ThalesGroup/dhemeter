from time import sleep
from rich.console import Console
from rich.table import Table
import subprocess
import os
import json

dict_response = {
    0: "Started",
    20: "Successfull",
    24: "No data found",
    40: "No variables selected",
    41: "No forecasts selected",
    42: "Run hour not available",
    50: "Error in request"
}



def docker_run(process_type, data_names, logs_dir, status):
    # list of data names logs
    logs_awaited = []
    # list of data names logs
    for data_name in data_names:
        logs_awaited.append("logs_"+data_name+".json")
    # with os list all the files in the logs dir
    files = os.listdir(logs_dir)
    # while all the log files awaited are not present in the logs dir
    while not all(file in files for file in logs_awaited):
        # list all the files in the logs dir
        files = os.listdir(logs_dir)
        # sleep 1 second
        sleep(1)
    # when all the log files awaited are present in the logs dir
    # stop the console status
    status.stop()
    return True

def exec_table(process_type, data_names, logs_dir):
    table = Table(title=process_type)
    table.add_column("Data_name")
    table.add_column("execution_status")
    table.add_column("attempts")
    table.add_column("successfull_attempts")
    table.add_column("execution_time")

    # logs awaited
    logs_awaited = []
    # list of data names logs
    for data_name in data_names:
        logs_awaited.append("logs_"+data_name+".json")
    # with os list all the files in the logs dir
    files = os.listdir(logs_dir)
    # while all the log files awaited are not present in the logs dir
    for file in files:
        if file in logs_awaited:
            with open(os.path.join(logs_dir, file)) as f:
                data = json.load(f)
                try:
                    execution_status = dict_response[data["execution_status"]]
                except:
                    execution_status = "Unknown Error"
                
                execution_time = str(data["execution_time"]) + " s"
                try:
                    table.add_row(data["Data_name"],execution_status , str(data["attempts"]), str(data["successfull_attempts"]), execution_time)
                except:
                    pass    
    console = Console()
    console.print(table)

def exec_table_nwp(process_type, data_names, logs_dir):
    table = Table(title=process_type)
    table.add_column("Data_name")
    table.add_column("execution_status")
    table.add_column("attempts")
    table.add_column("successfull_attempts")
    table.add_column("execution_time")

    # logs awaited
    logs_awaited = []
    # list of data names logs
    for data_name in data_names:
        logs_awaited.append("logs_"+data_name+".json")
    # with os list all the files in the logs dir
    files = os.listdir(logs_dir)
    # while all the log files awaited are not present in the logs dir
    for file in files:
        if file in logs_awaited:
            with open(os.path.join(logs_dir, file)) as f:
                data = json.load(f)
                try:
                    execution_status = dict_response[data["execution_status"]]
                except:
                    execution_status = "Unknown Error"
                
                execution_time = str(data["execution_time"]) + " s"
                try:
                    table.add_row(data["Data_name"],execution_status , str(data["attempts"]), str(data["successfull_attempts"]), execution_time)
                except:
                    pass    
    console = Console()
    console.print(table)

def exec_table_obs(process_type, data_names, logs_dir):
    table = Table(title=process_type)
    table.add_column("Data_name")
    table.add_column("execution_status")
    table.add_column("file_ratio")
    table.add_column("observation_ratio")
    table.add_column("execution_time")

    # logs awaited
    logs_awaited = []
    # list of data names logs
    for data_name in data_names:
        logs_awaited.append("logs_"+data_name+".json")
    # with os list all the files in the logs dir
    files = os.listdir(logs_dir)
    # while all the log files awaited are not present in the logs dir
    for file in files:
        if file in logs_awaited:
            with open(os.path.join(logs_dir, file)) as f:
                data = json.load(f)
                try:
                    execution_status = dict_response[data["execution_status"]]
                except:
                    execution_status = "Unknown Error"
                
                execution_time = str(data["execution_time"]) + " s"
                try:
                    table.add_row(
                                    data["Data_name"],
                                    execution_status , 
                                    str(data["file_successfull_attempts"])+"/"+str(data["file_attempts"]), 
                                    str(data["obs_successfull_attempts"])+"/"+str(data["obs_attempts"]), 
                                    execution_time
                                )
                except:
                    pass    
    console = Console()
    console.print(table)


def cdo_table(process_type, data_names, logs_dir):
    table = Table(title=process_type)
    table.add_column("execution_status")
    table.add_column("Data_name")

    # logs awaited
    logs_awaited = []
    # list of data names logs
    for data_name in data_names:
        logs_awaited.append("logs_"+data_name+".json")

    # with os list all the files in the logs dir
    files = os.listdir(logs_dir)
    # while all the log files awaited are not present in the logs dir
    for file in files:
        if file in logs_awaited:
            with open(os.path.join(logs_dir, file)) as f:
                data = json.load(f)
                try:
                    execution_status = dict_response[data["execution_status"]]
                except:
                    execution_status = "Unknown Error"
                try:
                    table.add_row(execution_status, data["Data_name"])
                except:
                    pass
    console = Console()
    console.print(table)

    
