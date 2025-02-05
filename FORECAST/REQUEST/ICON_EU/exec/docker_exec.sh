# parse the path of the instance directory and the configuration directory to the workflow
# 'sh ./MERGE/docker_exec.sh ' + instance_folder + ' ' + share_folder + ' ' + config_folder)

instance_dir=$1
share_dir=$2
config_dir=$3

# Check if the instance directory exists
if [ ! -d "$instance_dir" ]; then
    echo "The instance directory $instance_dir does not exist."
    exit 1
fi
#Check if the share directory exists
if [ ! -d "$share_dir" ]; then
    echo "The share directory $share_dir does not exist."
    exit 1
fi
#Check if the config directory exists
if [ ! -d "$config_dir" ]; then
    echo "The config directory $config_dir does not exist."
    exit 1
fi

data_dir="$instance_dir/data/raw"
logs_dir="$instance_dir/logs"
config_dir="$instance_dir/config"

docker run -v $data_dir:/home/app/data -v $logs_dir:/home/app/logs -v $config_dir:/home/app/config -v $share_dir:/home/app/share --user $UID:$(id -g) agregateur-forecast-request-icon_eu --logs_file "/home/app/logs/ICON_EU.log" --config_file "/home/app/share/config.json" --params_time "/home/app/config/params_time.json" --params_variables "/home/app/config/params_variables.json" --metaparams "/home/app/config/metaparams.json" --output_dir "/home/app/data" > $logs_dir/ICON_EU_out.log 2> $logs_dir/ICON_EU_err.log
#docker run -v $data_dir:/home/app/data -v $logs_dir:/home/app/logs -v $config_dir:/home/app/config -v $share_dir:/home/app/share -it satelite-request-sy_2_aod --logs_file "/home/app/logs/SY_2_AOD.log" --config_file "/home/app/share/config.json" --params_time "/home/app/config/params_time.json" --params_variables "/home/app/config/params_variables.json" --metaparams "/home/app/config/metaparams.json" --output_dir "/home/app/data" > $logs_dir/SY_2_AOD_out.log 2> $logs_dir/SY_2_AOD_err.log
