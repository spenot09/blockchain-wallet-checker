# Set base image (host OS)
FROM python:3.9-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /application

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip3 install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY wallet-checker .

# Specify the command to run on container start
#CMD [ "python", "./application.py" ]
ENV FLASK_APP=application.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
