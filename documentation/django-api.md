# Colegio Andolina
***
## Table of contents
1. [Main objective of this feature](#main-objective-of-this-feature)
2. [Technical approach](#technical-approach)
3. [Usage](#usage)
4. [Endpoints](#endpoints)
5. [Release features](#release-features)
6. [Credentials](#credentials)
***

<a name="main-objective-of-this-feature"></a>
## Main objective of this feature  

1. Use Django to build an API
2. Get access to all data to generate documents for school management

<a name="technical-approach"></a>
## Technical approach
1. Build several endpoints by model of the database
   1. first endpoint to get a list of all instances
   2. second endpoint to get  details of one specific instance of the model

<a name="usage"></a>
## Usage  
1. create your virtual env and install dependencies from requirements.txt
2. launch your virtual env
3. from the root repo:
   1. ``` python andolina/manage.py runserver```
4. when the server is running go to the several endpoints to perform the CRUD operations needed
   1. examples of CRUD operations with the file v1.utils.samples_api_requests.py
      1. modify the file of previous point 
      2. modify the method check_operations in the file v1.management.commands.operations_database.py (choose the test you want to perform)
      3. run this script ``` python andolina/manage.py operations_database ```
5. Play with the database following the credentials rules when creating new users ( please don't break it!)


<a name="endpoints"></a>
## Endpoints
#### list of all the action to perform, method to use and the associated URI

| ACTION PERFORMED                    | METHOD      | URI                                    |  
|-------------------------------------|-------------|----------------------------------------| 
| Get the list of all users           | GET / POST  | api/v1/users/                          |  
| Get a specific user details         | GET / PUT   | api/v1/users/{user_id}                 |  
| Get the list of all parents         | GET / POST  | api/v1/parents/                        |  
| Get a specific parent details       | GET / PUT         | api/v1/parents/{parent_id}             |  
| Get the list of all children        | GET / POST  | api/v1/children/                       |  
| Get a specific parent child         | GET / PUT         | api/v1/children/{child_id}             |  
| Get the list of all teachers        | GET  / POST | api/v1/teachers/                       |  
| Get a specific teacher details      | GET / PUT         | api/v1/teachers/{teacher_id}           |  
| Get the list of all school_groups   | GET  / POST | api/v1/school_groups/                  |  
| Get a specific school_group details | GET / PUT         | api/v1/school_groups/{school_group_id} |  
| Get the list of all documents       | GET  / POST | api/v1/documents/                      |  
| Get a specific document details     | GET / PUT         | api/v1/documents/{document_id}         |  

[here](https://documenter.getpostman.com/view/16015714/2s8YK9LR9B) is the Postman documentation with examples

<a name="release-features"></a>
## Release features
### 1. Release 1.3:
   #### the features tested are:
   1. Same as Release 1.2
   5. First API endpoint ready for tests


<a name="credentials"></a>
## Credentials

1. For [django admin site](http://127.0.0.1:8000/management/login/?next=/management/) the credentials are:
   1. login = admin
   2. password = andolina
2. For the new user creation please enter the same password for all: passwd_test
