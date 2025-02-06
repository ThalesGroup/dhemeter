# Définir les variables pour les chemins d'accès
FORECAST_PATH = FORECAST
#ARGO_INIT_PATH = ARGO/fetch-parameters
CLI_PATH = cli

# Nom des images Docker par catégorie
FORECAST_IMAGES = \
    agregateur-forecast-box \
    agregateur-forecast-clean_and_merge \
    agregateur-forecast-merge \
	agregateur-forecast-remap \
    agregateur-forecast-time_interp \
    agregateur-forecast-spatial_interp \
    agregateur-forecast-request-icon_global \
    agregateur-forecast-request-icon_eu \
    agregateur-forecast-request-ifs \
	agregateur-forecast-request-gfs

#ARGO_INIT_IMAGE = fetch-parameters

CLI_IMAGE = agregateur-cli

# Toutes les images
IMAGES = $(FORECAST_IMAGES) $(CLI_IMAGE) # $(ARGO_INIT_IMAGE)

# Règles principales
all: $(IMAGES)

forecast: $(FORECAST_IMAGES)
cli: $(CLI_IMAGE)

build: $(IMAGES)
build-forecast: forecast
build-cli: cli

##########################################################
######################## FORECAST ########################
##########################################################

agregateur-forecast-box:
	docker build -t agregateur-forecast-box $(FORECAST_PATH)/BOX/Docker

agregateur-forecast-clean_and_merge:
	docker build -t agregateur-forecast-clean_and_merge $(FORECAST_PATH)/CLEAN_AND_MERGE/Docker

agregateur-forecast-merge:
	docker build -t agregateur-forecast-merge $(FORECAST_PATH)/MERGE/Docker

agregateur-forecast-remap:
	docker build -t agregateur-forecast-remap $(FORECAST_PATH)/REMAP/Docker

agregateur-forecast-time_interp:
	docker build -t agregateur-forecast-time_interp $(FORECAST_PATH)/TIME_INTERP/Docker

agregateur-forecast-spatial_interp:
	docker build -t agregateur-forecast-spatial_interp $(FORECAST_PATH)/SPATIAL_INTERP/Docker

agregateur-forecast-request-icon_global:
	docker build -t agregateur-forecast-request-icon_global $(FORECAST_PATH)/REQUEST/ICON_GLOBAL/Docker

agregateur-forecast-request-icon_eu:
	docker build -t agregateur-forecast-request-icon_eu $(FORECAST_PATH)/REQUEST/ICON_EU/Docker

agregateur-forecast-request-ifs:
	docker build -t agregateur-forecast-request-ifs $(FORECAST_PATH)/REQUEST/IFS/Docker

agregateur-forecast-request-gfs:
	docker build -t agregateur-forecast-request-gfs $(FORECAST_PATH)/REQUEST/GFS/Docker

##########################################################
############################ CLI #########################
##########################################################
agregateur-cli:
	docker build -t agregateur-cli $(CLI_PATH)/Docker

##########################################################
########################### ARGO #########################
##########################################################
# \
fetch-parameters: \
	docker build -t fetch-parameters $(ARGO_INIT_PATH)/Docker \
# \
# Règle pour nettoyer les images Docker


##########################################################
########################### CLEAN ########################
##########################################################

clean:
	docker rmi $(IMAGES) || true
