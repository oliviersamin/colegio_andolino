import os
import time
import asyncio
import requests
from telegram import Bot, Document

from utils.credentials import (
    TOKEN_BOT_ANDOLINA_TEST,
    CHAT_ID_BOT,
    CHAT_ID_GROUP_COLEGIO_ANDOLINA,
)
from utils.constants import (
    DOWNLOAD_FOLDER_BASE_PATH,
    TEST_FILE_TO_UPLOAD
)


class CheckDownloadedFile:
    def __init__(self):
        self.document_number = len("")
        self.initial_directory = os.path.abspath(os.path.curdir)
        self.current_dir = self.initial_directory
        self.download_directory_path = DOWNLOAD_FOLDER_BASE_PATH[:-1]
        self.initial_downloaded_files = self.get_download_directory_files()
        self.message_reception_1_file = "The file has been downloaded successfully, thank you. It will be processed..."
        self.message_reception_several_files = "The files have been downloaded successfully, thank you. They will be processed..."

    def change_to_directory(self, directory_path: str) -> None:
        self.current_dir = directory_path
        return os.chdir(self.current_dir)

    def get_download_directory_files(self) -> list:
        if not self.current_dir == self.download_directory_path:
            self.change_to_directory(self.download_directory_path)
        return os.listdir(".")

    def get_new_downloaded_files(self) -> list:
        files = self.get_download_directory_files()
        if len(files) - len(self.initial_downloaded_files) > 0:
            diff = [item for item in files if item not in self.initial_downloaded_files]
            self.initial_downloaded_files = files
            return diff
        elif len(files) - len(self.initial_downloaded_files) < 0:
            self.initial_downloaded_files = self.get_download_directory_files()
        return []

    def delete_files_from_download_folder(self):
        files = os.listdir(os.curdir)
        file_to_keep = "test_file_to_upload.txt"
        commands = []
        for file in files:
            if file != file_to_keep:
                commands.append("rm " + "'" + file + "'")
        for command in commands:
            os.system(command)

    def check(self):
        files = self.get_new_downloaded_files()
        if len(files) == 1:
            return self.message_reception_1_file
        elif len(files) > 1:
            return self.message_reception_several_files
        return ""


class ChatBot:
    def __init__(self, chat_id, token_bot):
        self.chat_id = chat_id
        self.token_bot = token_bot
        self.bot = Bot(token=token_bot)

    async def send_message(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    async def send_document_from_local_storage(self, file_path):
        file = open(file_path, "rb")
        await self.bot.send_document(chat_id=self.chat_id, document=file)


async def main() -> None:
    """Start the non chat commands loop"""
    print("Commands script running...")
    DownloadedFiles = CheckDownloadedFile()
    Bot = ChatBot(chat_id=CHAT_ID_BOT, token_bot=TOKEN_BOT_ANDOLINA_TEST)

    # Function usefull to empty the download_temp_file in the docker volume except for the test_file
    # DownloadedFiles.delete_files_from_download_folder()
    while True:
        message = DownloadedFiles.check()
        if message:
            await Bot.send_message(message)
            await Bot.send_document_from_local_storage(TEST_FILE_TO_UPLOAD)
        time.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
