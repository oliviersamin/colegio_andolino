FROM python:3.8.10-slim-buster
WORKDIR /home/telegram
RUN apt update &&apt-get install build-essential -y

