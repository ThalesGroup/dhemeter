# INSTALL.md

## Prerequisites
### Required Software
- **Python 3.8+**
- **Docker** (for microservices containerization)
- **make**
- **jq**

---
## Installation

1. **Clone the repository** :
    ```bash
    git clone https://github.com/thalesgroup/dhemeter.git
    cd dhemeter
    ```
2. **Build Containers with Make** :
    - Build weather forecast-related containers
        ```bash
        make forecast
        ```
    - Build the CLI for API request configuration
        ```bash
        make cli
        ```
    - Build all project components (forecast, CLI, and additional services)
        ```bash
        make all
        ```
    - Remove all Docker images related to the project
        ```bash
        make clean
        ```
3. **Verify your installation** :
    ```bash
        docker images
    ```
    should return :

    ```bash
    REPOSITORY                                TAG       IMAGE ID       SIZE
    agregateur-cli                            latest    XXXXXXXXXX   262MB
    agregateur-forecast-request-ifs           latest    XXXXXXXXXX   123MB
    agregateur-forecast-request-icon_eu       latest    XXXXXXXXXX   123MB
    agregateur-forecast-request-icon_global   latest    XXXXXXXXXX   123MB
    agregateur-forecast-spatial_interp        latest    XXXXXXXXXX   451MB
    agregateur-forecast-time_interp           latest    XXXXXXXXXX   451MB
    agregateur-forecast-merge                 latest    XXXXXXXXXX   463MB
    agregateur-forecast-clean_and_merge       latest    XXXXXXXXXX   608MB
    agregateur-forecast-box                   latest    XXXXXXXXXX   451MB
    agregateur-forecast-remap                   latest    XXXXXXXXXX   451MB
    ```

You are now ready to go for a run : [README](./README.md)
