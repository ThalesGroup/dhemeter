# =============================================================================
# Copyright 2025 Thales Group
# Licensed under the APACHE 2 License. See LICENSE file in the project root for
# full license information.
# =============================================================================
FROM alexgleith/cdo

RUN mkdir /data/raw
RUN mkdir /data/out
RUN mkdir /data/config
RUN mkdir /data/logs

COPY ./app .

# sets the entrypoint for the container : this is the command that will be run when the container starts
# in this case, we run the python script
ENTRYPOINT ["python3", "interp.py"]
