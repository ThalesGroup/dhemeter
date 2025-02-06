# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
# 1. Base image python 3.8 alpine
FROM python:3.10-alpine

# 2. Set working directory
WORKDIR /home/app

RUN mkdir ./parameters

# 3. Copy requirements.txt to working directory
COPY ./requirements.txt ./installation/requirements.txt
# 4. Install dependencies
RUN pip install -r ./installation/requirements.txt

# 5. Copy the rest of the files to working directory
COPY ./app .

# 6. Run the app with the arguments: --workdir /home/app --params_folder parameters --metaparams_json metaparams.json --params_time_json params_time.json --params_variables_json params_variables.json
CMD ["python", "app.py", "--workdir", "/home/app", "--params_folder", "parameters", "--metaparams_json", "metaparams.json", "--params_time_json", "params_time.json", "--params_variables_json", "params_variables.json"]





