# 1. Base image 3.8.10-slim
FROM python:3.8.10-slim

# sets the working directory for the container : all commands will be run from this directory
WORKDIR /home/app

RUN mkdir ./config
RUN mkdir ./logs
RUN mkdir ./share
RUN mkdir ./data
RUN mkdir ./data/raw
RUN mkdir ./data/out
RUN mkdir ./data/tmp

# Copy the requirements.txt file to the home directory of the app user
COPY ./requirements.txt ./requirements.txt

# 3. Install dependencies
RUN pip install -r ./requirements.txt
RUN apt-get update
RUN apt-get install libeccodes-dev -y

# Copy the python script to the home directory of the app user
COPY ./app . 

# sets the entrypoint for the container : this is the command that will be run when the container starts
# in this case, we run the python script
ENTRYPOINT ["python", "extract.py"]