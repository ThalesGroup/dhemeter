
echo "Input downloading"
apt-get update && apt-get install -y curl
echo "Downloading the dataset"
mkdir tests_non_regression
cd tests_non_regression
mkdir -p ./data/input_CLEAN_AND_MERGE
cd ./data/input_CLEAN_AND_MERGE
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_CLEAN_AND_MERGE/IFS_merge_forecast_interp.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_CLEAN_AND_MERGE/ICON_GLOBAL_merge_forecast_interp.nc"


curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_CLEAN_AND_MERGE/ICON_EU_merge_forecast_interp.nc"
cd ../../
mkdir -p ./references/output_CLEAN_AND_MERGE
cd ./references/output_CLEAN_AND_MERGE
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_CLEAN_AND_MERGE/merge_time_interp_forecast.nc"

cd ../../
mkdir ./config
cd ./config
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/metaparams.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_time.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_variables.json"

cd ../
mkdir logs
mkdir -p outputs/output_CLEAN_AND_MERGE
cd ../../
