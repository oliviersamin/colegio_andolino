# Colegio Andolina
***
## Table of contents
1. [Main objective of this feature](#main-objective-of-this-feature)
2. [Technical approach](#technical-approach)
3. [Usage](#usage)
4. [Release features](#release-features)
5. [Credentials](#credentials)
***

<a name="main-objective-of-this-feature"></a>
## Main objective of this feature  

1. Use Django to build a database linked with Postgres
2. Use Django admin site to manage the school using the database
3. Use Django rest framework to build an API
4. Use Django to build later a website with forms to replace fastidious documents that need to be checked by parents


<a name="technical-approach"></a>
## Technical approach
1. Build an ERD to create the first database
2. Setup the admin site of Django to play with this database
3. Create an API to perform CRUD operations on the database from external scripts


<a name="usage"></a>
## Usage  
1. create your virtual env and install dependencies from requirements.txt
2. launch your virtual env
3. from the root repo:
   1. ``` python andolina/manage.py runserver```
4. when the server is running go to [this page](http://127.0.0.1:8000/management/login/?next=/management/) and enter the credentials for admin rights
5. Play with the database following the credentials rules when creating new users ( please dont break it!)

<a name="release-features"></a>
## Release features
### 1. Release 1.2:
   #### the features tested are:
   1. Same as Release 1.1
   2. Django admin site first setup to be tested and to be improved
   3. Database created with models Parent, Child, Teacher, Document, Group
   4. Database hosted online by ElephantSQL for tests only, 20 MB of free data max
   5. No API ready


<a name="credentials"></a>
## Credentials

1. For [django admin site](http://127.0.0.1:8000/management/login/?next=/management/) the credentials are:
   1. login = admin
   2. password = andolina
2. For the new user creation please enter the same password for all: passwd_test

