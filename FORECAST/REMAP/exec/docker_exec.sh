# parse the path of the instance directory and the configuration directory to the workflow
# 'sh ./MERGE/docker_exec.sh ' + instance_folder + ' ' + share_folder + ' ' + config_folder)

instance_dir=$1
share_dir=$2
config_dir=$3
model=$4

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
# check if the model is defined
if [ -z "$model" ]; then
    echo "The model is not defined."
    exit 1
fi

data_raw_dir="$instance_dir/data/raw"
data_out_dir="$instance_dir/data/out"
data_tmp_dir="$instance_dir/data/tmp"
logs_dir="$instance_dir/logs"
config_dir="$instance_dir/config"
# logs params is config_dir + /logs + _ + option (model)
logs_params="$logs_dir/$model.log"
#echo "docker run -v $data_raw_dir:/home/app/data/raw -v $data_out_dir:/home/app/data/out -v $data_tmp_dir:/home/app/data/tmp -v $logs_dir:/home/app/logs -v $config_dir:/home/app/config:ro -v $share_dir:/home/app/share -it forecast-merge --logs_file "/home/app/logs/MERGE_FORECAST.log" --config_file "/home/app/share/config.json" --params_time "/home/app/config/params_time.json" --params_variables "/home/app/config/params_variables.json" --metaparams "/home/app/config/metaparams.json" --output_dir "/home/app/data/out" --input_dir "/home/app/data/raw" --output_file "merge_forecast.nc" > $logs_dir/FORECAST_MERGE_out.log 2> $logs_dir/FORECAST_MERGE_err.log"
#echo "docker run -v $data_raw_dir:/data/raw -v $data_raw_dir:/data/out -v $data_tmp_dir:/data/tmp -v $logs_dir:/data/logs -v $config_dir:/data/config:ro -it forecast-remap --logs_file "/data/logs/REMAP.log" --logs_params "/data/logs/$model.log" --input_dir "/data/raw" --output_dir "/data/out" --option $model > $logs_dir/REMAP_out.log 2> $logs_dir/REMAP_err.log"
docker run -v $data_raw_dir:/data/raw -v $data_raw_dir:/data/out -v $data_tmp_dir:/data/tmp -v $logs_dir:/data/logs -v $config_dir:/data/config:ro --user $UID:$(id -g) agregateur-forecast-remap --logs_file "/data/logs/REMAP.log" --logs_params "/data/logs/$model.log" --input_dir "/data/raw/" --output_dir "/data/out/" --option $model > $logs_dir/REMAP_out.log 2> $logs_dir/REMAP_err.log
#docker run -v $data_raw_dir:/home/app/data/raw -v $data_out_dir:/home/app/data/out -v $data_tmp_dir:/home/app/data/tmp -v $logs_dir:/home/app/logs -v $config_dir:/home/app/config:ro -v $share_dir:/home/app/share -it --entrypoint /bin/bash satelite-merge