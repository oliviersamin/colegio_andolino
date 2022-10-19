"""
This script automatize all the steps to create docker images for telegram RPI 3 B+
It starts from scratch
"""

import argparse
import os
from constants import (
    DOCKER_BASE_IMAGE_NAME,
    DOCKER_TELEGRAM_SERVER_IMAGE_NAME,
    DOCKER_TELEGRAM_SERVER_IMAGE_FILE,
    DOCKER_BASE_IMAGE_FILE,
    DOCKER_COMPOSE_FILE,
)
from docker_images_utils import (
    telegram_image_exists,
    base_image_exists,
    unknown_image_exists,
)

CURRENT_FILE_PATH = __file__

COMMANDS = {
    "base":
        [
            "docker rmi -f {}".format(DOCKER_BASE_IMAGE_NAME),
            "docker build -f {} -t {} .".format(DOCKER_BASE_IMAGE_FILE, DOCKER_BASE_IMAGE_NAME)
        ],
    "telegram":
        [
            "docker rmi -f {}".format(DOCKER_TELEGRAM_SERVER_IMAGE_NAME),
            "docker build -f {} -t {} .".format(DOCKER_TELEGRAM_SERVER_IMAGE_FILE, DOCKER_TELEGRAM_SERVER_IMAGE_NAME),
            "docker-compose -f {} up chat commands".format(DOCKER_COMPOSE_FILE)
        ]
}


def parse_args():
    parser = argparse.ArgumentParser(description='Choose what docker image we want to create')
    parser.add_argument('--image', type=str, choices=["base", 'telegram', 'all'], default="telegram",
                        help='base image for telegram, telegram image or both images')

    args = parser.parse_args()
    return args


def clean_unknown_images():
    cleaning = unknown_image_exists()
    while cleaning != []:
        print("There is unknown image to clean...")
        command = "docker rmi -f " + cleaning[0]
        os.system(command)
        cleaning = unknown_image_exists()
    print("All the unknown images have been cleaned!")


def clean_all_stopped_containers():
    print("cleaning all stopped containers...")
    os.system("docker rm $(docker ps --filter status=exited -q)")


def create_images(image):
    if image == "telegram":
        if telegram_image_exists():
            commands = COMMANDS["telegram"]
        else:
            commands = COMMANDS["telegram"][1:]

        for command in commands:
            os.system(command)

    elif image == "base":
        if base_image_exists():
            commands = COMMANDS["base"]
        else:
            commands = COMMANDS["base"][1:]

        for command in commands:
            os.system(command)

    elif image == "all":
        if base_image_exists():
            commands = COMMANDS["base"]
            if telegram_image_exists():
                # commands += COMMANDS["telegram"]
                pass
            else:
                commands += COMMANDS["telegram"][1:]
        else:
            commands = COMMANDS["base"][1:]
            if telegram_image_exists():
                commands += COMMANDS["telegram"]
            else:
                commands += COMMANDS["telegram"][1:]
        for command in commands:
            os.system(command)


def main():
    image = parse_args().image
    clean_all_stopped_containers()
    clean_unknown_images()
    os.chdir(os.path.dirname(os.path.dirname(CURRENT_FILE_PATH)))
    create_images(image)


if __name__ == "__main__":
    main()
