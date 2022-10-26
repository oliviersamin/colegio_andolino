# Colegio Andolina
***
## Table of contents
1. [Main objective of this feature](#main-objective-of-this-feature)
2. [Technical approach](#technical-approach)
4. [Usage](#usage)
5. [Release features](#release-features)
***

<a name="main-objective-of-this-feature"></a>
## Main objective of this feature  

1. Use Telegram as a media of communication with the local server inside the school
2. Alternative way of communication if not possible to use a website

<a name="technical-approach"></a>
## Technical approach
1. Create a bot which will be admin in different chat group and will be abble to:
   1. answer questions of users
   2. download a file sent to the bot
   3. upload a file in a chat group when an external trigger is pull

2. Use docker to simplify reinstallation if needed

3. Docker containers will run in parallel to answer all the tasks needed 


<a name="usage"></a>
## Usage  
1. if you have both docker images named 'base_image_for_telegram' & 'telegram_server' go to the step 3
2. else:
   1. create your virtual env and install dependencies from requirements.txt
   2. launch your virtual env
   3. from the root repo
      1. open [utils/credentials](https://github.com/oliviersamin/colegio_andolino/blob/dev/utils/credentials.py) and change the value of CHAT_ID_BOT with your own chat id value
         1. help [here](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id) to find your chat id value
         2. the token bot value is named 'TOKEN_BOT_ANDOLINA_TEST' and is in the same credentials file than the CHAT_ID_BOT to modify
      2. run ``` python utils/create_docker_containers --image=<option>  ```
         1. if it is your first install option = all
         2. if you already have the docker image named 'base_image_for_telegram' but not the image named 'telegram_server' then your option = telegram
      3. At the end of the script, two containers are launched and the telegram feature is running 
3. if you want to start the telegram feature and you already have the containers then you should just start them ``` docker start telegram_chat telegram_commands```

<a name="release-features"></a>
## Release features
### 1. Release 1:
   #### the features tested are:
   1. reply automatically to a text message of a user in a chat when the user starts his message with "@bot"
   2. download automatically a document send by a user when he writes "@bot" into the caption section. A text message is sent in the chat when the file has been downloaded.

### 2. Release 1.1:
   #### the features tested are the same as previous release and one feature has been added: 
   1. when the user send a document with the same conditions, he receives the same text message and also a document that has been uploaded from local storage.
   This feature has just been added to check that we can upload a document from local storage to the chat.
   
