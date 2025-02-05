#!/bin/bash

# Check if an argument is passed
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/base/directory"
    exit 1
fi

# Base directory passed as parameter
base_dir="$1"

# Check if base directory exists
if [ ! -d "$base_dir" ]; then
    echo "Le répertoire de base $base_dir n'existe pas."
    exit 1
fi

# Generate unique ID
instance_id=$(date +"%Y%m%d%H%M%S")-$(uuidgen)

# Create instance root
instance_dir="$base_dir/$instance_id"
# set all permissions on the directory
# create the directory and all subdirectories for docker
mkdir -p "$instance_dir"


# Path to configuration file containing directory tree:
_dir=$(dirname "$0")
config_file="$_dir/../share/dir.conf"

# Check if configuration file exists
if [ ! -f "$config_file" ]; then
    echo "Le fichier de configuration $config_file n'existe pas."
    exit 1
fi

# Create directories from configuration file
while IFS= read -r line; do
    mkdir -p "$instance_dir/$line"
done < "$config_file"

# return the path of the created instance
echo "$instance_dir"