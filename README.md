# Colegio Andolina
***
## Table of contents
1. [Main objective of this repo](#main-objective-of-this-repo)
2. [Technical approach](#technical-approach)
3. [Architecture of IT project](#architecture-of-it-project)
4. [GitHub repo usage](#github-repo-usage)
5. [Releases](#releases)
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
2. Use various media of communication:
   1. Telegram, you can see all the details [here](documentation/Telegram.md)
   2. Django admin site, you can see all the details [here](documentation/django-server-api.md)
   3. Other media not defined yet

<a name="architecture-of-it-project"></a>
## Architecture of IT project 
So far an idea would be to use docker containers to realize the project.  
One container will be dedicated to Telegram aspect, one to Postgres, one to Django Rest Framework and one to CIVICRM.
This section will be modified along the project regarding the needs and new ideas.


<a name="github-repo-usage"></a>
## GitHub repo usage  
The several existing branches are for the following usage:
1. main = production purpose, the final users use it in a daily basis to manage school.
2. pre-production = stage where all the changes/features are tested by Fernando or any other parent to validate them before going to production (main)
3. dev = stage where each new feature developped is merged to be tested by the IT group of the school to validate features and changes before going to pre-production
4. feature/<name-of-feature> branch is made to develop a specific feature before sending it to dev branch. 
5. test-<name> is a branch created from a feature/<name-of-feature> branch to develop specific details before going to feature/<name-of-feature> branch

<a name="Releases"></a>
## releases are made on dev branch
### 1. Release 1:
   #### feature/telegram-basics:
   1. reply automatically to a text message of a user in a chat when the user starts his message with "@bot"
   2. download automatically a document send by a user when he writes "@bot" into the caption section. A text message is sent in the chat when the file has been downloaded.

### 2. Release 1.1:
   #### feature/telegram-basics:
1. features from release 1
2. when the user send a document with the same conditions, he receives the same text message and also a document that has been uploaded from local storage.  
This feature has just been added to check that we can upload a document from local storage to the chat.

