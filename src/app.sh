# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
# shell script that runs the aggregation process : 
# 1. Create the file structure calling the create_instance.sh script
# 2. Get the right workflow to run
# 3. Run the workflow with the right parameters

# Create the instance
# parse two arguments : the path to the configuration folder and the path to the instance folder
# verify that the arguments are passed
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 /path/to/config/directory /path/to/instance/directory"
    exit 1
fi

# Configuration directory
config_dir="$1"
# Instance directory
instance_dir="$2"

# Check if the configuration directory exists
if [ ! -d "$config_dir" ]; then
    echo "The configuration directory $config_dir does not exist."
    exit 1
fi

# Check if the instance directory exists
if [ ! -d "$instance_dir" ]; then
    echo "The instance directory $instance_dir does not exist."
    exit 1
fi

# Create the instance : execute the create_instance.sh script in the same directory as this script
current_dir=$(dirname "$0")
# aggregator_dir is one folder up from the current directory
aggregator_dir=$(dirname "$current_dir")
echo "Aggregator directory: $aggregator_dir"
# share directory is in the aggregator directory + share
share_dir="$aggregator_dir/share"
instance_dir=$(bash "$current_dir/create_instance.sh" "$instance_dir")

echo "Instance created in $instance_dir"
# copy the configuration files to the instance directory in the configuration folder
cp -r "$config_dir"/* "$instance_dir/config"


# in the config folder, there is a file called metaparams.json that contains the main parameters of the workflow
# we need to parse this file to get the right workflow to run
metaparams_file="$instance_dir/config/metaparams.json"
if [ ! -f "$metaparams_file" ]; then
    echo "The file $metaparams_file does not exist."
    exit 1
fi

# Parse the metaparams.json file : jq is a command-line JSON processor
workflow=$(jq -r '.workflow' "$metaparams_file")
if [ -z "$workflow" ]; then
    echo "The workflow is not defined in the file $metaparams_file."
    exit 1
fi
# in the json file, there is a key called "SOURCE" that contains the workflow to run : check which workflow to run and if it is not defined, exit
workflow_source=$(jq -r '.SOURCE' "$metaparams_file")
echo "Workflow to run: $workflow_source"

# go to the workflow directory : which is the aggregator directory + the workflow source
workflow_dir="$aggregator_dir/$workflow_source"
if [ ! -d "$workflow_dir" ]; then
    echo "The workflow directory $workflow_dir does not exist."
    exit 1
fi

# Run the workflow
# execute the app.py script in the workflow directory
# parse the configuration directory and the instance directory as arguments
# try to run the workflow

echo "Running the workflow..."
# run the app.py script in the workflow directory : parse the configuration directory and the instance directory and the share directory as arguments
# execute the python script like : python3 app.py -c /path/to/config/directory -i /path/to/instance/directory -s /path/to/share/directory
python3 "$workflow_dir/app.py" -c "$instance_dir/config" -i "$instance_dir" -s "$share_dir"
# check the return code of the python script
if [ $? -ne 0 ]; then
    echo "An error occurred while running the workflow."
    exit 1
fi

