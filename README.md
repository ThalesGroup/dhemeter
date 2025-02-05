# README.md
## Description
DHEMETER: Data Hub for Environmental and METEorological Resources is an open-source tool designed to centralize and aggregate meteorological data from multiple APIs and providers (NOAA, ECMWF, Météo France, DWD, etc.). The project unifies this data into a coherent and homogeneous format (NetCDF), providing a single file that consolidates meteorological information.

The tool uses a microservices-based architecture to manage data processing pipelines. It is designed to be extensible and scalable, facilitating the integration of new data sources or features.

---

## Main Features
- **Data Aggregation**: Merges data from multiple providers.
- **Format Normalization**: Standardizes meteorological data to NetCDF format.
- **Geographic Selection**: Allows filtering data by region.
- **Advanced Processing**:
  - Spatial and temporal interpolations.
  - Configurable queries using JSON dictionaries.
- **Real-time Monitoring**: Graphical interface to monitor workflows and retrieve intermediate data.

## Description and Prerequisites

In order to install the DHEMETER tool, please follow the [Installation Instructions](./INSTALL.md)

## Setup a Run

Setup an API request trough 3 JSON files :
```bash
├── metaparams.json : contains the general parameters about the request
├── params_time.json : contains the time parameters about the request
└── params_variables.json : contains the variables parameters about the request
```

Setup your configuration directory for the API REQUEST, run the CLI and then let the program guide you:
```bash
mkdir params
docker run -it -v ./params:/home/app/parameters agregateur-cli
```
Once you finished the request the following files will be created, these files are mandatory for running a request:
```bash
params
├── metaparams.json
├── params_time.json
└── params_variables.json
```

See examples in [Request Examples](./config)

## Run Dhemeter

To run the program, you need to use the following command, for now we will use absolute path to the request files :

```bash
sh ./src/app.sh <absolute_path_to_your_config_folder> <absolute_path_to_your_output_folder>
```

General Request example, let's consider that ``params`` contains JSON API arguments :
```bash
mkdir RUN
sh ./src/app.sh $(pwd)/params $(pwd)/RUN
```

Instance's path will be returned in CLI

## Output

The execution of the program will create a folder structure in the output folder. 
The entry point is the id of the request's execution, it will return a directory file name in ``./RUN/<datetime>-<uniqueid>`` :
```bash
<datetime>-<uniqueid>
├── config
│   ├── metaparams.json
│   ├── params_time.json
│   └── params_variables.json
├── data
│   ├── out
│   ├── raw
│   └── tmp
└── logs
```


The data folder contains the output of the request :
- out : the final outputs of the request
- raw : the raw outputs of the request (without any processing)
- tmp : the temporary files created during the request execution

The logs folder contains the logs of the request execution.

The config folder contains the request files used for the execution.

The output files are in the netCDF format and can be used for further analysis : AIRD, post-processing, etc.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors

DHEMETER has been created by [Thales Group](https://www.thalesgroup.com/fr)