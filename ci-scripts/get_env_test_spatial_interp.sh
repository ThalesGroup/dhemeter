echo "Input downloading"
apt-get update && apt-get install -y curl
echo "Downloading the dataset"
mkdir tests_non_regression
cd tests_non_regression
mkdir -p ./data/input_SPATIAL_INTERP
cd ./data/input_SPATIAL_INTERP
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_SPATIAL_INTERP/merge_time_interp_forecast.nc"
cd ../../
mkdir -p ./references/output_SPATIAL_INTERP
cd ./references/output_SPATIAL_INTERP
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_SPATIAL_INTERP/merge_spatial_interp_forecast.nc"
cd ../..
echo "Configuration files downloading"

mkdir config
cd config


curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/metaparams.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_time.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_variables.json"

cd ../
mkdir logs
mkdir -p outputs/output_SPATIAL_INTERP
cd ../../