"""
Module contains class to test employee api.
"""
from department_app.tests.conftest import BaseTestCase, create_app


class TestDEmployeeApi(BaseTestCase):
    """
    Class for employee api test cases.
    """

    # Tests for GET requests
    def test_employees_get_all(self):
        """
        Test get request.
        """
        response = self.client.get("/api/v1/employees")
        assert response.status_code == 200
        assert len(response.json) == 10

    def test_employees_get_with_id(self):
        """
        Test get by id request.
        """
        emp_id = 3
        response = self.client.get(f"/api/v1/employees/{emp_id}")
        assert response.status_code == 200
        assert response.json["id_"] == emp_id

    def test_employees_get_with_nonexistent_id(self):
        """
        Test get request with incorrect data (emp_id).
        """
        wrong_id = 42
        response = self.client.get(f"/api/v1/employees/{wrong_id}")
        assert response.status_code == 404
        assert f"Employee with id = {wrong_id} was not found" in response.json["message"]

    # Tests for POST requests
    def test_employees_post(self):
        """
        Test post request with correct data.
        """
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1994-04-05",
            "salary": 500,
            "department_id": 1,
        }
        response = self.client.post("/api/v1/employees", json=data)
        assert response.status_code == 201
        assert response.json["salary"] == 500

    def test_employees_post_wrong_data(self):
        """
        Test post request with incorrect data.
        """
        data = {
            "full_name": "New Employee",
            "date_of_birth": "Not a Date",
            "salary": 500,
        }
        response = self.client.post("/api/v1/employees", json=data)
        assert response.status_code == 400

    def test_employees_post_nonexistent_department_id(self):
        """
        Test post request with incorrect data (wrong dep_id).
        """
        client = create_app().test_client()
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1994-04-05",
            "salary": 500,
            "department_id": 42,
        }
        response = client.post("/api/v1/employees", json=data)
        assert response.status_code == 400
        assert response.json["message"] == "Not valid department id"

    def test_employees_post_with_id(self):
        """
        Test post request (wrong method for url).
        """
        emp_id = 1
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1994-04-05",
            "salary": 500,
            "department_id": 1,
        }
        response = self.client.post(f"/api/v1/employees/{emp_id}", json=data)
        assert response.status_code == 405

    # Tests for PUT requests
    def test_employees_put_without_id(self):
        """
        Test put request with incorrect data (not given emp_id).
        """
        data = {
            "full_name": "Employee 1 updated",
            "date_of_birth": "1994-04-05",
            "salary": 1001,
            "department_id": 1,
        }
        response = self.client.put("/api/v1/employees/", json=data)
        assert response.status_code == 405

    def test_employees_put_with_id(self):
        """
        Test put request with correct data.
        """
        emp_id = 1
        data = {
            "full_name": "Employee updated",
            "date_of_birth": "1994-04-05",
            "salary": 1001,
            "department_id": 1,
        }
        response = self.client.put(f"/api/v1/employees/{emp_id}", json=data)
        assert response.status_code == 200
        assert response.json["full_name"] == "Employee updated"

    def test_employees_put_with_nonexistent_id(self):
        """
        Test put request with incorrect data (wrong emp_id).
        """
        wrong_id = 42
        data = {
            "full_name": "Employee updated",
            "date_of_birth": "1994-04-05",
            "salary": 1001,
            "department_id": 1,
        }
        response = self.client.put(f"/api/v1/employees/{wrong_id}", json=data)
        assert response.status_code == 404
        assert f"Employee with id {wrong_id} not found" in response.json["message"]

    def test_employees_put_with_id_incomplete_data(self):
        """
        Test put request with incorrect data.
        """
        emp_id = 1
        data = {
            "full_name": "Employee 1 updated",
            "date_of_birth": "1994-04-05",
        }
        response = self.client.put(f"/api/v1/employees/{emp_id}", json=data)
        assert response.status_code == 400

    # def test_employees_put_with_id_nonexistent_department_id(self):
    #     """
    #     Test put request with incorrect data (wrong dep_id).
    #     """
    #     client = create_app().test_client()
    #     emp_id = 1
    #     data = {
    #         "full_name": "Employee updated",
    #         "date_of_birth": "1994-04-05",
    #         "salary": 1001,
    #         "department_id": 42
    #     }
    #     response = client.put(f"/api/v1/employees/{emp_id}", json=data)
    #     assert response.status_code == 400
    #     assert response.json["message"] == "Not valid department id"

    # Tests for DELETE requests
    def test_employees_delete_without_id(self):
        """
        Test delete request (not given emp_id).
        """
        response = self.client.delete("/api/v1/employees")
        assert response.status_code == 405

    def test_employees_delete_with_id(self):
        """
        Test delete request.
        """
        emp_id = 1
        response = self.client.delete(f"/api/v1/employees/{emp_id}")
        assert response.status_code == 204
        assert len(response.data) == 0

    def test_employees_delete_with_nonexistent_id(self):
        """
        Test delete request (wrong emp_id).
        """
        wrong_id = 42
        response = self.client.delete(f"/api/v1/employees/{wrong_id}")
        assert response.status_code == 404
        assert f"Employee with id = {wrong_id} was not found" in response.json["message"]

    # Tests for EmployeesSearchAPI

    # Tests for searching all employees
    def test_employees_search_no_querystring(self):
        """
        Test get request (without data).
        """
        response = self.client.get("/api/v1/employees/search")
        assert response.status_code == 400
        assert response.json["message"] == "Enter search data"

    def test_employees_search_one_querystring(self):
        """
        Test get request with 1 argument.
        """
        date_to_search = "1991-01-01"
        response = self.client.get(f"/api/v1/employees/search?date_of_birth={date_to_search}")
        assert response.status_code == 200
        assert all(emp["date_of_birth"] == date_to_search for emp in response.json)

    def test_employees_search_two_querystrings(self):
        """
        Test get request with 2 arguments.
        """
        date_to_search = "1991-01-01"
        date_to_search_2 = "1999-09-09"
        response = self.client.get(
            f"/api/v1/employees/search?date_of_birth={date_to_search}&date_for_interval={date_to_search_2}"
        )
        assert response.status_code == 200
        assert all(
            date_to_search <= emp["date_of_birth"] <= date_to_search_2
            for emp in response.json
        )

    # Tests for searching employees in department

    def test_departments_employees_search_no_querystring(self):
        """
        Test get request (without data).
        """
        response = self.client.get("/api/v1/departments/1/employees/search")
        assert response.status_code == 400
        assert response.json["message"] == "Enter search data"

    def test_departments_employees_search_one_querystring(self):
        """
        Test get request with 1 argument from department.
        """
        date_to_search = "1991-01-01"
        response = self.client.get(
            f"/api/v1/departments/1/employees/search?date_of_birth={date_to_search}"
        )
        assert response.status_code == 200
        assert all(emp["date_of_birth"] == date_to_search for emp in response.json)

    def test_departments_employees_search_two_querystrings(self):
        """
        Test get request with 2 arguments from department.
        """
        dep_id = 1
        date_to_search = "1991-01-01"
        date_to_search_2 = "1999-09-09"
        response = self.client.get(
            f"/api/v1/departments/{dep_id}/employees/search?date_of_birth={date_to_search}&date_for_interval={date_to_search_2}"
        )
        assert response.status_code == 200
        assert all(
            date_to_search <= emp["date_of_birth"] <= date_to_search_2
            for emp in response.json
        )

    def test_departments_employees_search_one_querystring_nonexistent_department(self):
        """
        Test get request with 1 argument from not existing department.
        """
        wrong_dep_id = 42
        date_to_search = "1991-01-01"
        response = self.client.get(
            f"/api/v1/departments/{wrong_dep_id}/employees/search?date_of_birth={date_to_search}"
        )
        assert response.status_code == 404
        assert f"Department with id {wrong_dep_id} not found" in response.json["message"]
