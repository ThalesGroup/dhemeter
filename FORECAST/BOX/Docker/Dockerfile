FROM alexgleith/cdo

RUN mkdir /data/input
RUN mkdir /data/output
RUN mkdir /data/config
RUN mkdir /data/logs

COPY ./app .

# sets the entrypoint for the container : this is the command that will be run when the container starts
# in this case, we run the python script
ENTRYPOINT ["python3", "box.py"]