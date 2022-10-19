"""
This script automatize all the steps to create docker images for telegram RPI 3 B+
It starts from scratch
"""

import os

PATH_BASE_TELEGRAM = "/home/ospgd/Andolina/colegio_andolino"
DOCKERFILE_BASE_IMAGE_FILE = "Dockerfile_to_create_base_image"
DOCKERFILE_BASE_IMAGE_NAME = "base_image_for_telegram:v1.0"
DOCKERFILE_TELEGRAM_SERVER_IMAGE_FILE = "Dockerfile_to_create_telegram_basics"
DOCKERFILE_TELEGRAM_SERVER_IMAGE_NAME = "telegram_server:v1.0"
DOCKER_COMPOSE_FILE = "telegram.yaml"

commands = [
    "docker rmi -f {}".format(DOCKERFILE_BASE_IMAGE_NAME),
    "cd {}".format(PATH_BASE_TELEGRAM),
    "docker build -f {} -t {} .".format(DOCKERFILE_BASE_IMAGE_FILE, DOCKERFILE_BASE_IMAGE_NAME),
    "docker build -f {} -t {} .".format(DOCKERFILE_TELEGRAM_SERVER_IMAGE_FILE, DOCKERFILE_TELEGRAM_SERVER_IMAGE_NAME),
    "docker-compose -f {} up chat commands".format(DOCKER_COMPOSE_FILE),

]


for command in commands:
    os.system(command)
