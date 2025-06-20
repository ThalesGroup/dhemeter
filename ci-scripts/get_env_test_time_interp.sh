echo "Input downloading"
apt-get update && apt-get install -y curl
echo "Downloading the dataset"
mkdir tests_non_regression
cd tests_non_regression
mkdir -p ./data/input_TIME_INTERP
cd ./data/input_TIME_INTERP

curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_TIME_INTERP/IFS_merge_forecast.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_TIME_INTERP/ICON_GLOBAL_merge_forecast.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_TIME_INTERP/ICON_EU_merge_forecast.nc"

cd ../../
mkdir -p ./references/output_TIME_INTERP

cd ./references/output_TIME_INTERP

curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_TIME_INTERP/IFS_merge_forecast_interp.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_TIME_INTERP/ICON_GLOBAL_merge_forecast_interp.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_TIME_INTERP/ICON_EU_merge_forecast_interp.nc"

cd ../../

mkdir logs
mkdir config

cd config
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/metaparams.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_time.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_variables.json"

cd ../
mkdir -p ./outputs/output_TIME_INTERP