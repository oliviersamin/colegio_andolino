FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get upgrade -y && apt-get install -y locales

# Set the locale
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

# Install texlive necesary packages
RUN apt-get install -y texlive-latex-extra

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt /
RUN cd /
RUN python -m pip install -r requirements.txt

COPY utils/scripts /app/utils/scripts
