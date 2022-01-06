# pylint: disable=E0602
"""Module defines department and employee REST API.."""
from flask_restful import Api

import department_app.rest.department_rest
import department_app.rest.employee_rest

api = Api(prefix='/api/v1')

"""Functions register the routes with the framework using the given endpoints."""

# Department resources

api.add_resource(
    department_rest.DepartmentApi,
    '/departments',
    methods=['GET', 'POST'],
    endpoint='departments',
    strict_slashes=False
)

api.add_resource(
    department_rest.DepartmentApi,
    '/departments/<dep_id>',
    methods=['GET', 'PUT', 'DELETE'],
    endpoint='department',
    strict_slashes=False
)

api.add_resource(
    department_rest.DepartmentsEmployeesApi,
    '/departments/<dep_id>/employees',
    methods=['GET', 'POST'],
    strict_slashes=False
)

# Employee resources

api.add_resource(
    employee_rest.EmployeeApi,
    '/employees',
    endpoint='employees',
    methods=['GET', 'POST'],
    strict_slashes=False
)

api.add_resource(
    employee_rest.EmployeeApi,
    '/employees/<emp_id>',
    endpoint='employee',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)

# Search resource

api.add_resource(
    employee_rest.EmployeeSearchApi,
    '/employees/search',
    '/departments/<dep_id>/employees/search',
    methods=['GET'],
    strict_slashes=False
)
