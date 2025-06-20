# Workflow paths 
FORECAST_PATH = FORECAST
REANALYSIS_PATH = REANALYSIS
#ARGO_INIT_PATH = ARGO/fetch-parameters
CLI_PATH = cli

# Docker images 
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

REANALYSIS_IMAGES = \
    agregateur-reanalysis-request-era5_pressure_levels \
    agregateur-reanalysis-request-era5_single_level \
    agregateur-reanalysis-merge 

#ARGO_INIT_IMAGE = fetch-parameters

CLI_IMAGE = agregateur-cli

# Docker Images
IMAGES = $(FORECAST_IMAGES) $(REANALYSIS_IMAGES) $(CLI_IMAGE) # $(ARGO_INIT_IMAGE)

# Rules
all: $(IMAGES)
reanalysis: $(REANALYSIS_IMAGES)
forecast: $(FORECAST_IMAGES)
cli: $(CLI_IMAGE)

build: $(IMAGES)
build-forecast: forecast
build-reanalysis: reanalysis
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
######################## REANALYSIS ######################
##########################################################

agregateur-reanalysis-request-era5_pressure_levels:
	docker build --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) -t agregateur-reanalysis-request-era5_pressure_levels $(REANALYSIS_PATH)/REQUEST/ERA5_PRESSURE_LEVELS/Docker

agregateur-reanalysis-request-era5_single_level:
	docker build --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) -t agregateur-reanalysis-request-era5_single_level $(REANALYSIS_PATH)/REQUEST/ERA5_SINGLE_LEVEL/Docker

agregateur-reanalysis-merge:
	docker build -t agregateur-reanalysis-merge $(REANALYSIS_PATH)/MERGE/Docker


##########################################################
############################ CLI #########################
##########################################################
agregateur-cli:
	docker build -t agregateur-cli $(CLI_PATH)/Docker


# Default parameter directory
PARAMS_DIR ?= $(CURDIR)/params
OUTPUT_DIR ?= $(CURDIR)/output

create-config:
	@echo "📁 Checking if $(PARAMS_DIR) exists..."
	@if [ ! -d "$(PARAMS_DIR)" ]; then \
		echo "📂 Directory $(PARAMS_DIR) does not exist. Creating it..."; \
		mkdir -p "$(PARAMS_DIR)"; \
		chown $(UID):$(shell id -g) "$(PARAMS_DIR)"; \
	fi

	@echo "🔧 Creating request configuration using Command Line Interface..."
	@docker run -it --rm \
		--user $(UID):$(id -g) \
		-v $(PARAMS_DIR):/home/app/parameters \
		$(CLI_IMAGE)

	@echo "\n✅ Configuration process completed."
	@echo "📁 Generated files are available on the host at: $(PARAMS_DIR)"
	@tree $(PARAMS_DIR)

run:
	@test -f ./src/app.sh || (echo "❌ Error: ./src/app.sh not found" && exit 1)
	@test -d $(PARAMS_DIR) || (echo "❌ Error: Config directory $(PARAMS_DIR) does not exist" && exit 1)

	@mkdir -p $(OUTPUT_DIR)
	@OUTPUT_DIR_REALPATH=$$(realpath $(OUTPUT_DIR)) && \
	PARAMS_DIR_REALPATH=$$(realpath $(PARAMS_DIR)) && \
	echo "🚀 Running Dhemeter with config from: $$PARAMS_DIR_REALPATH" && \
	echo "📤 Output will be saved to: $$OUTPUT_DIR_REALPATH" && \
	sh ./src/app.sh $$PARAMS_DIR_REALPATH $$OUTPUT_DIR_REALPATH && \
	echo "\n✅ Dhemeter execution finished." && \
	echo "📁 Check output folder: $$OUTPUT_DIR_REALPATH" && \
	tree $$OUTPUT_DIR_REALPATH


##########################################################
########################### CLEAN ########################
##########################################################

clean:
	docker rmi $(IMAGES) || true

clean-env:
	@rm -f ./share/env.sh
	@echo "🧹 ./share/env.sh deleted"


##########################################################
########################### CONNECT ######################
##########################################################


.PHONY: print-env-vars

print-env-vars:
	@echo "📋 Available Environment Variables for DHEMETER:"
	@echo ""
	@echo "🔑 DHEMETER_CDS_API_KEY:"
	@echo "    → Required to connect to the CDS (Climate Data Store) API (ERA5 access)."
	@echo "    → Usage:"
	@echo "       export DHEMETER_CDS_API_KEY=your-key"
	@echo ""
	@echo "📝 Notes:"
	@echo "    - If not provided, the system will try to load it from ./share/env.sh."
	@echo "    - You can predefine it in a local script like ./share/env.sh:"
	@echo "        export DHEMETER_CDS_API_KEY=your-key"
	@echo ""
	@echo "💡 Tip:"
	@echo "    To apply your key manually, run:"
	@echo "        source ./share/env.sh"
