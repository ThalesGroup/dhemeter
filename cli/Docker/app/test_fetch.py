import os

# create a string with the parameters
stringParamsVariables = "'"+'{"variable1": "value1", "variable2": "value2"}'+ "'"
stringParamsTime = "'"+'{"time": "2021-01-01T00:00:00Z"}' + "'"

print(stringParamsVariables)

# create a file with the parameters
filenameParamsVariables = "params_variables.json"
filenameParamsTime = "params_time.json"

# create a directory to store the parameters
output_dir = "output"
output_path = "/home/app/output"

# build the container image
os.system("docker build -t fetch-params:latest ./fetch-params/Docker")

# run the container with a volume to store the parameters
run_command = "docker run -v $(pwd)/" + output_dir + ":" + output_path + " fetch-params:latest " + stringParamsVariables + " " + filenameParamsVariables + " " + stringParamsTime + " " + filenameParamsTime + " " + output_path
print(run_command)
os.system(run_command)

