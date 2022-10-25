# Colegio Andolina
***
## Table of contents
1. [Main objective of this repo](#main-objective-of-this-repo)
2. [Technical approach](#technical-approach)
3. [Architecture of IT project](#architecture-of-it-project)
4. [Usage](#usage)
5. [Manuals](#manuals)
6. [Credentials](#credentials)
***

<a name="main-objective-of-this-repo"></a>
## Main objective of this repo  

1. Help the actual coordinator of the school to gain time and be more efficient in his tasks
2. Help any other Circle of the school in its process to gain time & efficiency
3. Finding technical solutions without asking more money to families

<a name="technical-approach"></a>
## Technical approach

### The money criteria is crucial so we are focusing on open-source / free solutions

#### Hardware aspect:
1. getting school's own server to stock the database & communicate with parents
    technical solution possible: Raspberry Pi inside the school with internet connection

#### Software aspect:
1. Create a database from the actual data inside the existing excel sheets. 
2. Use Telegram to communicate from anywhere outside the school to the server to do actions:
    a. ask it informations (messages)
    b. send documents to be downloaded & to be processed to be stored in the database
    c. receive documents that have been generated such as Excel files
    d. manage permissions regarding the different circles by allowing different actions in different groups of 
    Telegram in which the biot is always an admin

<a name="architecture-of-it-project"></a>
## Architecture of IT project 
 So far an idea would be to use docker containers to realize the project.  
One container will be dedicated to Telegram aspect, one to Postgres, one to Django Rest Framework and one to CIVICRM.
This section will be modified along the project regarding the needs and new ideas.


<a name="usage"></a>
## Usage  
When an update is made to the branch dev, the test can be performed with the following steps:
1. create a chat with the bot on telegram to perform tests
2. Get the ID of this chat
3. in the utils.credentials file modify the value of CHAT_ID_BOT with the chat ID
4. To create for the first time the docker images and launch the containers use the following command form the root folder of the repo:  
`python3.9 utils/create_docker_containers --image=all`   It creates two images.  
5. The first one is a basis to then create the telegram image. It has been done this way because it takes time to create the first image and when updates are made to the project it is just to the telegram part. It is just saving time when developping.
6. Report to the corresponding manual section to know how to use the version of the dev release

<a name="manuals"></a>
## Manuals
### 1. Release 1 of dev:
   #### the features tested are:
   1. reply automatically to a text message of a user in a chat when the user starts his message with "@bot"
   2. download automatically a document send by a user when he writes "@bot" into the caption section. A text message is sent in the chat when the file has been downloaded.

### 2. Release 1.1 of dev:
   #### the features tested are the same as previous release and one feature has been added: 
   1. when the user send a document with the same conditions, he receives the same text message and also a document that has been uploaded from local storage.
   This feature has just been added to check that we can upload a document from local storage to the chat.
    
<a name="credentials"></a>
## Credentials
For the Django admin site:
superuser:
login = admin
password = andolina

all users:
password = passwd_test
