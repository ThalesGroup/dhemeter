apt-get update && apt-get install -y curl
echo "Downloading the dataset"
mkdir tests_non_regression
cd tests_non_regression
mkdir config data logs
cd config
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/config/metaparams.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/config/params_variables.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/config/params_time.json"
cd ../data
mkdir input_BOX
cd input_BOX
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/data/input_BOX/merge_spatial_interp_forecast.nc"
cd ../../
mkdir -p outputs/output_BOX
mkdir -p references/output_BOX
cd references/output_BOX
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/references/output_BOX/merge_box_forecast.nc"
cd ../../../
ls -lR ./tests_non_regression