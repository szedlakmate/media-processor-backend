# File uploader example

The purpose of this project is demonstrating the backend logic of a file processor server.

This example project is based on an existing repo: https://github.com/axelpale/minimal-django-file-upload-example.git

The project was written using python3 with Django. Please note that the project mostly contains the backend elements of
the demonstrated functionality.

The project contains an OpenAPI documentation with the implemented endpoints and their usages.
For detailed description, please read **openapi.yaml**

## Setup 

The app can be started in 2 ways. Before that download the project from https://github.com/szedlakmate/media-processor-backend.git

### Using Docker

The given dockerfile handles the app configuration
First building the project:
> docker build -t serverapp .

Then the app can be started using docker, binding the ports as given below:
> docker run -p 8000:8000 --name serverapp serverapp

Notice that the SQLite db file is not saved when using docker.
This limitation can be solved for example using docker-compose with a volume mount but it is not in the scope of this work.

### Using local environment

The project is written in python 3.8 and support python 3.6+. The project shall be run on a debian based OS with ffmpeg installed.
If the above conditions are met, please also install the given requirements.txt using:
> pip3 install -r requirements.txt

Before starting up the project, initiate data models by running the Django migrations:
> python3 manage.py migrate

Then the app can be started:
> python3 manage.py runserver

## Usage

1) To upload a file open http://127.0.0.1:8000 and submit the form.
The response contains a reference ID of the uploaded RawFile
1) To start encoding the uploaded file use the */packaged_content* endpoint as given in the openapi doc.
The response contains reference of the new converted media.
1) To check the status of the conversion the */packaged_content/<reference_id>* endpoint can be used.
The responses are described in the api doc.
