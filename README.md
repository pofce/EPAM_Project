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