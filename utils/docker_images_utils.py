import os
from constants import (
    DOCKER_BASE_IMAGE_NAME,
    DOCKER_TELEGRAM_SERVER_IMAGE_NAME
)


def get_docker_images():
    data_string = os.popen("docker images").readlines()
    data_list = [line.split(" ") for line in data_string]
    result = []
    for line in data_list:
        result.append([])
        for item in line:
            if item:
                result[-1].append(item)
    return result[1:]


def base_image_exists() -> bool:
    data = get_docker_images()
    for line in data:
        tag = line[0] + ":" + line[1]
        if tag == DOCKER_BASE_IMAGE_NAME:
            return True
    return False


def telegram_image_exists() -> bool:
    data = get_docker_images()
    for line in data:
        tag = line[0] + ":" + line[1]
        if tag == DOCKER_TELEGRAM_SERVER_IMAGE_NAME:
            return True
    return False


def unknown_image_exists():
    data = get_docker_images()
    for line in data:
        tag = line[0] + ":" + line[1]
        if tag == "<none>:<none>":
            return [line[2]]
    return []
