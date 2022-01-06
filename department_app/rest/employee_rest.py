"""
Module contains Flask-Restful Resources for Employees
and for EmployeesSearch.
"""
from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from department_app.rest.schemas import EmployeeSchema
from department_app.service import EmployeeServices, DepartmentServices


class EmployeeApi(Resource):
    """
    This class defines the EmployeeApi Resource, available at the
    "/api/v1/employees/[<int:id>]" url
    """
    emp_schema = EmployeeSchema()

    def get(self, emp_id=None):
        """
        This method is called when GET request is sent to "/api/v1/employees/[<int:id>]" url
        :return:
        if "id" not specified => the list of all employees in json format, status code 200.
        If "id" specified =>  the list of employees from specified department serialized to json,
        status code 200.
        If invalid "id" => error message, status code 404.
        """
        if emp_id is None:
            employees = EmployeeServices.get_all()
            return self.emp_schema.dump(employees, many=True), 200
        employee = EmployeeServices.get_by_id(emp_id)
        if employee is None:
            return {'message': f'Employee with id = {emp_id} was not found'}, 404
        return self.emp_schema.dump(employee), 200

    def post(self):
        """
        This method is called when POST request is sent to "/api/v1/employees" url with json data.
        Creates a new employee entry in database.
        :return:
        if valid data provided => returns the created entry serialized to json, status code 201
        if invalid data => returns the error message in json format, status code 400.
        """
        json_data = request.get_json(force=True)
        try:
            data = self.emp_schema.load(json_data)
        except ValidationError as exception:
            return 'Bad data', 400
        try:
            new_employee = EmployeeServices.create(data)
        except IntegrityError:
            return {'message': 'Not valid department id'}, 400
        return self.emp_schema.dump(new_employee), 201

    def put(self, emp_id):
        """
        This method is called when GET request is sent to "/api/v1/employees/id" url with json data.
        Changes specified data of selected employee in database.
        :return:
        if valid data provided => returns the changed entry serialized to json, status code 200
        if invalid data => error message in json format, status code 400.
        If invalid "id" => error message, status code 404.
        """
        json_data = request.get_json(force=True)
        employee = EmployeeServices.get_by_id(emp_id)
        if employee is None:
            return {'message': f"Employee with id {emp_id} not found"}, 404
        try:
            data = self.emp_schema.load(json_data, partial=True)
        except ValidationError as exception:
            return exception.messages, 400
        try:
            updated_employee = EmployeeServices.update(employee, data)
        except IntegrityError:
            return {'message': 'Not valid department id'}, 400
        return self.emp_schema.dump(updated_employee), 200

    @staticmethod
    def delete(emp_id):
        """
        This method is called when DELETE request is sent to url "/api/v1/employees/id"
        deletes employee with specified "id" from database.
        :return:
        if valid "id" => returns an empty response body and status code 204 specified.
        If invalid "id" specified => returns error message and status code 404.
        """
        employee = EmployeeServices.get_by_id(emp_id)
        if employee is None:
            return {'message': f'Employee with id = {emp_id} was not found'}, 404
        EmployeeServices.delete(employee)
        return '', 204


class EmployeeSearchApi(Resource):
    """
    This class defines the EmployeeSearchApi Resource, available at the
    "/api/v1/employees/search" url
    """
    search_schema = EmployeeSchema()

    def get(self, dep_id=None):
        """
        This method is called when GET request is sent to:
        "/api/v1/employees/search" or
        :return:
        if "date_for_interval" not specified => the list of all employees who were born on
        "date_of_birth" in json format, status code 200.
        If "date_for_interval" specified =>  the list of all employees who were born in interval
        in json format, status code 200.
        If invalid "date_of_birth" => error message, status code 400.

        "/api/v1//departments/<dep_id>/employees/search" urls.
        :return:
        if "date_for_interval" specified => the list of all employees who were born on
        "date_of_birth" from specified department in json format, status code 200.
        if "date_for_interval" not specified => the list of all employees who were born in interval
        from specified department in json format, status code 200.
        If invalid "dep_id" => error message, status code 404.
        """
        date_of_birth = request.args.get('date_of_birth')
        if date_of_birth is None:
            return {'message': 'Enter search data'}, 400
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        date_for_interval = request.args.get('date_for_interval')
        if date_for_interval:
            date_for_interval = datetime.strptime(date_for_interval, "%Y-%m-%d").date()
        if dep_id is None:
            employees = EmployeeServices.get_by_date_of_birth(date_of_birth, date_for_interval)
        else:
            department = DepartmentServices.get_by_id(dep_id)
            if department is None:
                return {"message": f"Department with id {dep_id} not found"}, 404
            employees = EmployeeServices.get_by_date_of_birth_from_department(
                dep_id,
                date_of_birth,
                date_for_interval
            )

        return self.search_schema.dump(employees, many=True), 200
