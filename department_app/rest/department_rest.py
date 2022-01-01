"""
Module contains Flask-Restful Resources for Departments.
"""
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from department_app.service import DepartmentServices, EmployeeServices
from department_app.rest.schemas import DepartmentSchema, EmployeeSchema


class DepartmentApi(Resource):
    """
    This class defines the DepartmentsAPI Resource, available at the
    "/api/v1/departments/[<int:id>]" url
    """
    dep_schema = DepartmentSchema()

    def get(self, dep_id=None):
        """
        This method is called when GET request is sent to "/api/v1/departments/[<int:id>]" url
        :return:
        if "id" not specified => the list of all departments in json format, status code 200.
        If "id" specified =>  the department with the specified "id" serialized to json, status code 200.
        If invalid "id" => error message, status code 404.
        """
        if dep_id is None:
            departments = DepartmentServices.get_all()
            return self.dep_schema.dump(departments, many=True), 200
        department = DepartmentServices.get_by_id(dep_id)
        if department is None:
            return {'message': f'Department with id = {dep_id} was not found'}, 404
        return self.dep_schema.dump(department), 200

    def post(self):
        """
        This method is called when POST request is sent to "/api/v1/departments" url with json data.
        Creates a new department entry in database.
        :return:
        if valid data provided => returns the created entry serialized to json, status code 201
        if invalid data => returns the error message in json format, status code 400.
        """
        json_data = request.get_json(force=True)
        try:
            data = self.dep_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            new_department = DepartmentServices.create(data)
        except IntegrityError:
            return {'message': 'Department names should be unique'}, 400
        return self.dep_schema.dump(new_department), 201

    def put(self, dep_id):
        """
        This method is called when GET request is sent to "/api/v1/departments/id" url with json data.
        Changes name of specified department in database.
        :return:
        if valid data provided => returns the changed entry serialized to json, status code 200
        if invalid data => returns the error message in json format, status code 400.
        If invalid "id" => error message, status code 404.
        """
        json_data = request.get_json(force=True)
        department = DepartmentServices.get_by_id(dep_id)
        if department is None:
            return {'message': f'Department with id = {dep_id} was not found'}, 404
        try:
            data = self.dep_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 400
        try:
            updated_department = DepartmentServices.update(department, data)
        except IntegrityError:
            return {'message': 'Department names should be unique'}, 400
        return self.dep_schema.dump(updated_department), 200

    @staticmethod
    def delete(dep_id):
        """
        This method is called when DELETE request is sent to url "/api/v1/departments/id"
        deletes the department entry with specified id from database.
        :return:
        if valid "id" => returns an empty response body and status code 204 specified.
        If invalid "id" specified => returns error message and status code 404.
        """
        department = DepartmentServices.get_by_id(dep_id)
        if department is None:
            return {'message': f'Department with id = {dep_id} was not found'}, 404
        DepartmentServices.delete(department)
        return '', 204


class DepartmentsEmployeesApi(Resource):
    """
    This class defines the DepartmentsEmployeesAPI Resource, available at the
    "/api/v1/departments/[<int:id>]/employees" url
    """
    emp_schema = EmployeeSchema()

    def get(self, dep_id):
        """
        This method is called when GET request is sent to "/api/v1/departments/[<int:id>]/employees" url
        :return:
        If "id" is valid => list of employees from department with specified "id" serialized to json, status code 200.
        If invalid "id" => error message, status code 404.
        """
        department = DepartmentServices.get_by_id(dep_id)
        if department is None:
            return {'message': f'Department with id = {dep_id} was not found'}, 404
        employees = EmployeeServices.get_all_from_department(dep_id)
        return self.emp_schema.dump(employees, many=True), 200

    def post(self, dep_id):
        """
        This method is called when POST request is sent to "/api/v1/departments/[<int:id>]/employees" url with json data.
        Creates a new employee in specified department in database.
        :return:
        if valid data provided => returns the created entry serialized to json, status code 201
        if invalid data => returns the error message in json format, status code 400.
        if invalid "id" => returns the error message in json format, status code 404.
        """
        json_data = request.get_json(force=True)
        department = DepartmentServices.get_by_id(dep_id)
        if department is None:
            return {'message': f'Department with id = {dep_id} was not found'}, 404
        try:
            data = self.emp_schema.load(json_data, partial=["department_id"])
        except ValidationError as e:
            return e.messages, 400
        data['department_id'] = dep_id
        new_employee = EmployeeServices.create(data)
        return self.emp_schema.dump(new_employee), 201
