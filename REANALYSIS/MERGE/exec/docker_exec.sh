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

data_raw_dir="$instance_dir/data/raw"
data_out_dir="$instance_dir/data/out"
data_tmp_dir="$instance_dir/data/tmp"
logs_dir="$instance_dir/logs"
config_dir="$instance_dir/config"
output_file="merge_reanalysis.nc"
execution_file="MERGE_REANALYSIS.log"


docker run  -v $data_raw_dir:/home/app/data/raw \
            -v $data_out_dir:/home/app/data/out \
            -v $data_tmp_dir:/home/app/data/tmp \
            -v $logs_dir:/home/app/logs \
            -v $config_dir:/home/app/config:ro \
            -v $share_dir:/home/app/share \
            --user $UID:$(id -g) \
            agregateur-reanalysis-merge \
            --execution_file "/home/app/logs/${execution_file}" \
            --params_variables "/home/app/config/params_variables.json" \
            --params_time "/home/app/config/params_time.json" \
            --output_dir "/home/app/data/out" \
            --output_file $output_file \
            --input_dir "/home/app/data/raw" \
            > $logs_dir/REANALYSIS_MERGE_out.log 2> $logs_dir/REANALYSIS_MERGE_err.log


echo $output_file
echo $execution_file
echo $logs_dir