# EPAM_Project
External course Python Project

[![Build Status] (https://app.travis-ci.com/github/pofce/EPAM_Project)](https://app.travis-ci.com/github/pofce/EPAM_Project)

[![Coverage Status] (https://coveralls.io/github/pofce/EPAM_Project)](https://coveralls.io/github/pofce/EPAM_Project)

## Description
A simple web application for managing departments and employees. Uses REST-API
for CRUD operations. Allows to:

- display all departments, and the average salary for these departments.
- display all employees with their information(name, date of birth, salary,
  department).
- display employees in a particular department.
- search employees born on a specified date or in an interval between dates,
  both among all employees and employees of a particular department.
- add, update and delete departments and employees.

## Structure

1) errors - this package includes modules with error handlers
2) forms - this package includes modules with forms for html templates
3) models - this package includes modules with Python classes describing DB models
4) rest - this package includes modules with RESTful service implementation
5) service - this package includes modules with functions to work with DB (CRUD operations)
6) templates - html templates
7) tests - this package includes modules with unit tests
8) views - this package includes modules with Web controllers / views

## Installation
### First  way:
1. Clone this repo:

        git clone git clone https://github.com/pofce/EPAM_Project

2. Proceed to the EPAM_Project directory:
 
        cd EPAM_Project

3. Run the "install_and_run.sh" script:
      
       ./run.sh

4. Once everything has started up, you should be able to access the app with test data added at
   [http://127.0.0.1:5000/](http://0.0.0.0:5000/) on your host machine. If it doesn't work try 
   second way of installing.

### Second way:

1. Clone this repo:

        git clone https://github.com/pofce/EPAM_Project
2. Set up and activate the virtual environment: (optionally)
    ```
    virtualenv venv
    source env/bin/activate
    ```
3. Install the requirements:
    ```
    pip install -r requirements.txt
    ```
4. Configure MySQL database. Open config.py and find:
    ```
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://<DB_PORT>:<DB_PASSWORD>@<DB_HOST>/<DB_USERNAME>"
    ```
5. Set the following environment variables:
    ```
    DB_USERNAME=<your database username>
    DB_PASSWORD=<your database password>
    DB_HOST=<your database host>
    DB_PORT=<your database port>
    ```
You can set these in .env file as the project uses dotenv module to load 
environment variables.

6. Run migrations to create database infrastructure:
    ```
    flask db upgrade
    ```
7. Run the project locally:
    ```
    python -m flask run
    ```
   or
    ```
    python wsgi.py
    ```

## API endpoints

* "/api/v1/departments"
    * GET - get all departments.
    * POST - create new department. Data:
      ```json 
      {"title": <str>}
      ```
    
* "/api/v1/departments/<dep_id>"
    * GET - get department by id. Returns json with department id, department name,
      list of employees and average salary.
    * PUT - update department. Data:
      ```json 
      {"title": <str>}
      ```
    * DELETE - delete department with all its employees.
  

* "/api/v1/departments/<dep_id>/employees"
    * GET - get all employees in specified department.
    * POST - create a new employee in specified department. Data(all fields required):
      ```json
      {"full_name": <str>, "date_of_birth": "%Y-%m-%d" <str>, "salary": <int>}
      ```
      

* "/api/v1/employees"
    * GET - get all employees
    * POST - create a new employee. Data (every field required):
      ```json
      {"full_name": <str>, "date_of_birth": <"%Y-%m-%d" str>, "salary": <int>, "department": <str>}
      ```
      
* "/api/v1/employees/<emp_id>"
    * GET - get employee by id.
    * PUT - update employee. Data (all fields required):
      ```json 
      {"name": <str>, "birthday": <"%Y-%m-%d" str>, "salary": <int>, "dep_id": <int>}
      ```
    * DELETE - delete employee by id  
  

* "/api/v1/employees/search"
    * GET - search for employees born on a specified date or in an
      interval among all employees. Data:
      
       * query parameters: ?date_of_birth=<%Y-%m-%d>&[date_for_interval=<%Y-%m-%d>]


* "/api/v1/departments/<dep_id>/employees/search""
    * GET - search for employees born on a specified date or in an
      interval among all employees of the specified department. Data:
      
      * query parameters: ?date_of_birth=<%Y-%m-%d>&[date_for_interval=<%Y-%m-%d>]
