
# Introduction

The main purpose is to upload a file of cities and then search by their name and admin_name 

### Preconditions

Ensure to get unused the next ports:

* 9200
* 8000
* 5434
* 6379

If you want to keep using those ports 
you must to change their values on docker-compose.yml file

# Initialize

To start the application:

    $ cp base/.env.example base/.env
    $ docker-compose up
    
You must keep open the terminal in order to see the application logs

And then initialize the database in another shell 

    $ docker-compose exec cities python manage.py migrate
    $ docker-compose restart django-q

The second command will ensure that the scheduler has their migrations loaded
The application is ready to receive requests on port 8000
      

# Usage

Next we have the main features.

#### 1. Upload cities

Replace *[file_location]* with the full path of the file. 
A file example [here](https://drive.google.com/file/d/1qF2OuiLviWcfazaU97sOYWdCMfWrAXg0/view?usp=sharing)

    $ curl --request POST 'http://localhost:8000/cities/upload/' --form 'file=@"[file_location]"'


The application will store the cities on postgresql and elasticsearch asynchronously using redis

    

#### 2. List cities with pagination

    $ curl -X GET 'http://localhost:8000/cities?page=1'

You can change the *page* param to get more data.

#### 3. Search for cities by name and admin_name

    $ curl -X GET 'http://localhost:8000/cities/search/?q=Cauca'

You can change the *q* param to get more data. For example Cali or Buena
