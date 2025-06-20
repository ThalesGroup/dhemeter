# README.md
## Description
DHEMETER: Data Hub for Environmental and METEorological Resources is an open-source tool designed to centralize and aggregate meteorological data from multiple APIs and providers (NOAA, ECMWF, Météo France, DWD, etc.). The project unifies this data into a coherent and homogeneous format (NetCDF), providing a single file that consolidates meteorological information.
The software is distributed under the Apache license (see LICENSE.md) and uses third-party libraries that are distributed under their own terms (see THIRD_PARTY_LICENSES.md).

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

## Connecting to Data Providers

Some data providers (e.g., ECMWF) require authentication credentials. To set your cds credentials for example, use the following command:

```bash
export DHEMETER_CDS_API_KEY=your-api-key
```
Get a quick overview of environment variables for service connection capabilities. Run this command to see the list of variables you need to provide:

```bash
make print-env-vars
```

## Creating a Configuration

DHEMETER uses a set of configuration files (JSON format) to define the request to be sent to the data providers.

To create a configuration interactively, use the following `make` command:

```bash
make create-config
```
This will:

- Create the configuration directory (default: ./params) if it doesn't exist.
- Launch the configuration CLI in a Docker container.
- Store generated files in the mounted directory.

You can customize the configuration and output directories like so:

make create-config PARAMS_DIR=./myparams

After completion, the following structure will be created in ./params:

```bash
params
├── metaparams.json
├── params_time.json
└── params_variables.json
```

See examples in [Request Examples](./config)

## Run Dhemeter

Once your request configuration is ready, you can run the program with:

```bash
make run
```

By default, it will use:

`./params` as the configuration directory
`./output` as the output directory

You can override these paths with for instance :

```bash
make run PARAMS_DIR=./config/UC1/config_rea OUTPUT_DIR=./output
```

##  Outputs

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