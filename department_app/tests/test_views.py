"""Module contains pytest fixtures to run views tests with"""
import threading
import time

import pytest
from flask import request

from department_app import create_app, db
from department_app.models.population import populate_bd
from config import TestConfig


@pytest.fixture(scope="module")
def module_app():
    """
    Pytest fixture to make app, application test context
    and db populated with test data available in tests.
    Module scope to make server work in view tests.
    """
    _app = create_app(config_class=TestConfig)
    ctx = _app.test_request_context()
    ctx.push()
    _app.testing = True

    with _app.app_context():
        db.create_all()
        populate_bd()

    yield _app
    ctx.pop()


# testing department views


@pytest.fixture(scope="module")
def mclient(module_app):
    """
    A pytest fixture to make a test client available
    in tests. Module scope to make server work in view tests.
    """
    client = module_app.test_client()
    yield client


def shutdown_server():
    """
    Helper function to shut down the test server in the "server"
    pytest fixture.
    """
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@pytest.fixture(scope="module")
def server(module_app):
    """
    Pytest fixture to make app running ass a server during
    test. This makes possible to send requests from view functions
    to api endpoints in tests.
    """

    @module_app.route("/shutdown", methods=("POST",))
    def shutdown():
        shutdown_server()
        return "Shutting down server ..."

    t = threading.Thread(target=module_app.run)
    time.sleep(3)
    yield t.start()

    import requests

    requests.post("http://localhost:5000/shutdown")


# testing department views


def test_departments_list_view_get(module_app, mclient, server):
    """
    Test '/departments' route for get request
    """
    time.sleep(2)
    response = mclient.get("/departments")
    assert response.status_code == 200
    assert b"Departments" in response.data


def test_departments_list_view_post(module_app, mclient, server):
    """
    Test '/departments' route for post request
    """
    data = {"title": "PHP"}
    response = mclient.post("/departments", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"created successfully" in response.data


def test_departments_list_view_post_wrong_data(module_app, mclient, server):
    """
    Test '/departments' route for get request with wrong data
    """
    data = {"title": "D"}
    response = mclient.post("/departments", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"must be between 3 and 128 characters long" in response.data


def test_department_detail_view_get(module_app, mclient, server):
    """
    Test '/departments/{dep_id}' route for get request
    """
    response = mclient.get("/departments/1")
    assert response.status_code == 200
    assert b"Python" in response.data


def test_department_detail_view_get_wrong_id(module_app, mclient, server):
    """
    Test '/departments/{dep_id}' route for get request with wrong "dep_id"
    """
    response = mclient.get("/departments/42")
    assert response.status_code == 404
    assert b"not found" in response.data


def test_create_employee_for_department_post(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/employees' route for post request
    """
    time.sleep(2)
    data = {
        "full_name": "New Employee",
        "date_of_birth": "1999-05-04",
        "salary": 555,
    }
    response = mclient.post(
        "/departments/1/employees", data=data, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"successfully" in response.data


def test_create_employee_for_department_post_wrong_data(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/employees' route for post request with wrong data
    """
    data = {
        "full_name": "Employee New",
        "date_of_birth": "1999-05-04",
        "salary": 0,
    }
    response = mclient.post(
        "/departments/1/employees", data=data, follow_redirects=True
    )
    assert response.status_code == 200
    assert b"required" in response.data


def test_department_edit_view_get(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/edit' route for get request
    """
    response = mclient.get("/departments/1/edit")
    assert response.status_code == 200


def test_department_edit_view_get_wrong_id(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/edit' route for get request with wrong "dep_id"
    """
    response = mclient.get("/departments/42/edit")
    assert response.status_code == 404
    assert b"not found" in response.data


def test_department_edit_view_post(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/edit' route for post request
    """
    data = {"title": "Python UPD"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully" in response.data


def test_department_edit_view_post_fails_validation(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/edit' route for post request with wrong data
    """
    data = {"title": "P"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 3 and 128 characters long." in response.data


def test_department_edit_view_post_duplicate_name(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/edit' route for post request with wrong data
    """
    data = {"title": "C++"}
    response = mclient.post("/departments/1/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"be unique" in response.data


def test_department_delete_view_get(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/delete' route for get request
    """
    response = mclient.get("/departments/1/delete", follow_redirects=True)
    assert response.status_code == 200
    assert b"successfully." in response.data


def test_department_delete_view_get_wrong_id(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/delete' route for get request wit wrong dep_id
    """
    response = mclient.get("/departments/42/delete")
    assert response.status_code == 404
    assert b"not found" in response.data


# testing employee views


def test_employees_list_view_get(module_app, mclient, server):
    """
    Test '/employees' route for get request
    """
    response = mclient.get("/employees")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_list_view_post(module_app, mclient, server):
    """
    Test '/employees' route for post request
    """
    data = {
        "full_name": "New Employee",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 1,
    }
    response = mclient.post("/employees", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_employees_list_view_post_wrong_data(module_app, mclient, server):
    """
    Test '/employees' route for post request with wrong data.
    """
    data = {
        "full_name": "E",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 2,
    }
    response = mclient.post("/employees", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 6 and 128 characters long." in response.data


def test_employee_edit_view_get(module_app, mclient, server):
    """
    Test '/employees/{emp_id}/edit' route for get request.
    """
    response = mclient.get("/employees/3/edit")
    assert response.status_code == 200


def test_employee_edit_view_get_wrong_id(module_app, mclient, server):
    """
    Test '/employees/{emp_id}/edit' route for get request with wrong "emp_id".
    """
    response = mclient.get("/employees/42/edit")
    assert response.status_code == 404
    assert b"not found" in response.data


def test_employee_edit_view_post(module_app, mclient, server):
    """
    Test '/employees/{emp_id}/edit' route for post request.
    """
    data = {
        "full_name": "Employee Update",
        "date_of_birth": "1999-05-04",
        "salary": 90000,
        "department_id": 1,
    }
    response = mclient.post("/employees/3/edit", data=data, follow_redirects=True)
    assert response.status_code == 200


def test_employee_edit_view_post_fails_validation(module_app, mclient, server):
    """
    Test '/employees/{emp_id}/edit' route for post request with bad data.
    """
    data = {
        "full_name": "E",
        "date_of_birth": "1999-05-04",
        "salary": 555,
        "department_id": 2,
    }
    response = mclient.post("/employees/3/edit", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Field must be between 6 and 128 characters long." in response.data


def test_employee_delete_view_get_wrong_id(module_app, mclient, server):
    """
    Test '/employees/{emp_id}/edit' route for get request with wrong "emp_id".
    """
    response = mclient.get("/employees/42/delete")
    assert response.status_code == 404
    assert b"not found" in response.data


def test_employees_search_view_without_dep_id_one_date(module_app, mclient, server):
    """
    Test '/employees/search' route for get request with 1 argument.
    """
    response = mclient.get("/employees/search?date_of_birth=1994-04-05")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_without_dep_id_two_dates(module_app, mclient, server):
    """
    Test '/employees/search' route for get request with 2 arguments.
    """
    response = mclient.get(
        "/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_dep_id_one_date(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/employees/search' route for get request with 1 argument.
    """
    response = mclient.get("/departments/3/employees/search?date_of_birth=1994-04-05")
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_dep_id_two_dates(module_app, mclient, server):
    """
    Test '/departments/{dep_id}/employees/search' route for get request with 2 arguments
    """
    response = mclient.get(
        "/departments/3/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 200
    assert b"Employees" in response.data


def test_employees_search_view_with_invalid_dep_id_two_dates(
    module_app, mclient, server
):
    """
    Test '/departments/{dep_id}/employees/search' route for get request with 2 arguments and wrong "dep_id"
    """
    response = mclient.get(
        "/departments/42/employees/search?date_of_birth=1994-04-05&date_for_interval=2000-01-01"
    )
    assert response.status_code == 404
    assert b"not found" in response.data
