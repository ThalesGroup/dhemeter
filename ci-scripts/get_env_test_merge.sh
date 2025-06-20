echo "Input downloading"
apt-get update && apt-get install -y curl
echo "Downloading the dataset"
mkdir tests_non_regression
cd tests_non_regression
mkdir -p ./data/input_MERGE
cd ./data/input_MERGE
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/IFS_20250604_00_3.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_1000_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/IFS_20250604_00_0.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_006.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_850_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_1000_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_005.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_850_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_v_10m_single-level_heightAboveGround_None_001.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_v_pressure-level_isobaricInhPa_925_003.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/ICON_EU_u_pressure-level_isobaricInhPa_925_004.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/remaped_ICON_GLOBAL_u_10m_single-level_heightAboveGround_None_002.grib2"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./data/input_MERGE/IFS_20250604_00_6.grib2"

cd ../../
echo "Reference downloading"

mkdir -p ./references/output_MERGE
cd ./references/output_MERGE
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_MERGE/IFS_merge_forecast.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_MERGE/ICON_GLOBAL_merge_forecast.nc"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./references/output_MERGE/ICON_EU_merge_forecast.nc"
cd ../../
mkdir -p outputs/output_MERGE

echo "Configuration files downloading"

mkdir config
cd config


curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/metaparams.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_time.json"
curl -u $ARTIFACTORY_USER:$ARTIFACTORY_TOKEN -O "https://artifactory.thalesdigital.io/artifactory/private-docker-aes-datavalo/floria/tests_non_regression/./config/params_variables.json"

cd ../
mkdir logs/
cd ../../
