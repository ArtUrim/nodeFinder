# use python container image
From python:3.11.2

# set the working directory of the image filesystem 
WORKDIR /node_connector

# copy current directory to the working directory 
ADD . /node_connector

# Install the python dependencies
RUN pip install -r requirements.txt

# start the uWSGI
CMD ["uwsgi", "node_con.ini"]
