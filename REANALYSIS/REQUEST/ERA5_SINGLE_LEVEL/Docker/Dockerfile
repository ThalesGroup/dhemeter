# 1. Base image 3.8.10-slim
FROM python:3.8.10-slim

# sets the working directory for the container : all commands will be run from this directory
WORKDIR /home/app

RUN mkdir ./config
RUN mkdir ./logs
RUN mkdir ./share
RUN mkdir ./data

# Copy the requirements.txt file to the home directory of the app user
COPY ./requirements.txt ./installation/requirements.txt

#Install dependencies
RUN pip install -r ./installation/requirements.txt

# Copier le fichier .env
COPY .env .env

# Copy the python script to the home directory of the app user
COPY ./app ./ERA5_SINGLE_LEVEL 

# Ajouter le chemin source au PYTHONPATH
ENV PYTHONPATH="/home/app/"

# sets the entrypoint for the container : this is the command that will be run when the container starts
# in this case, we run the python script
ENTRYPOINT ["python", "ERA5_SINGLE_LEVEL/request.py"]


# Create a user with the specified UID and GID
ARG UID
ARG GID
RUN groupadd -g ${GID} cdsgroup && useradd -m -u ${UID} -g cdsgroup cdsuser
RUN chown -R ${UID}:${GID} "/home/app/"
# Set the default user
USER ${UID}:${GID}
