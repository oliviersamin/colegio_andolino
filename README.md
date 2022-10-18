# Colegio Andolina
***
## Table of contents
1. [Main objective of this repo](#main-objective-of-this-repo)
2. [Technical approach](#technical-approach)
3. [Architecture of IT project](#architecture-of-it-project)
4. [Usage](#usage)
5. [Actual issues](#actual-issues)
***

<a name="main-objective-of-this-repo"></a>
## Main objective of this repo  

1. Help the actual coordinqtor of the school to gain time and be more efficient in his tasks
2. Help any other Circle of the school in its processess to gain time & efficicency
3. Findinf technical solutions without asking more money to families

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
When an update is made to the GitHub repo, one makes manually:
1. the creation of the docker image using the Dockerfile_from_scratch_to_telegram_server_ready file
2. Use then the docker-compose file telegram.yaml to launch the containers with the following command:
`docker-compose -f telegram.yaml up chat commands`

<a name="actual-issues"></a>
## Actual Issues
1. The program is running in local without using the containers using the following steps:
   1. on a first tab in the virtual env run `python chat.py`
   2. on a second tab in the virtual env run `python commands.py`
   3. The program is running properly

With docker containers, modification must be made to ensure a communication between the 2 scripts probably through
get and post requests


