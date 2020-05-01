FROM python:3.8.2-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y ffmpeg

EXPOSE 8000

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py migrate

ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
