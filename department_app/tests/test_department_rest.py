"""
Module contains class to test department api.
"""
from distutils.version import LooseVersion


from department_app.tests.conftest import BaseTestCase, create_app


class TestDepartmentApi(BaseTestCase):
    """
    Class for department api test cases.
    """

    client = create_app().test_client()

    # Tests for GET requests
    def test_departments_get_all(self):
        """
        Test get request.
        """
        response = self.client.get("/api/v1/departments")
        assert response.status_code == 200
        assert len(response.json) == 3

    def test_departments_get_with_id(self):
        """
        Test get by id request.
        """
        response = self.client.get("/api/v1/departments/1")
        assert response.status_code == 200
        assert response.json["title"] == "Python"

    def test_departments_get_with_nonexistent_id(self):
        """
        Test get request with incorrect data (dep_id).
        """
        wrong_id = 42
        response = self.client.get(f"/api/v1/departments/{wrong_id}")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for POST requests
    def test_departments_post(self):
        """
        Test post request with correct data.
        """
        data = {"title": "PHP"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 201
        assert response.json["title"] == "PHP"

    def test_departments_post_wrong_data(self):
        """
        Test post request with incorrect data.
        """
        data = {"name": "PHP"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 400

    def test_departments_post_duplicate_name(self):
        """
        Test post request with incorrect data (repeated title).
        """
        data = {"title": "Python"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 400
        assert "Department names should be unique" in response.json["message"]

    def test_departments_post_with_id(self):
        """
        Test post request with incorrect url.
        """
        data = {"title": "Css"}
        response = self.client.post("/api/v1/departments/1", json=data)
        assert response.status_code == 405

    # Tests for PUT requests
    def test_departments_put_without_id(self):
        """
        Test put request with incorrect data (not given dep_id).
        """
        data = {"title": "Python+"}
        response = self.client.put("/api/v1/departments/", json=data)
        assert response.status_code == 405

    def test_departments_put_with_id(self):
        """
        Test put request with correct data.
        """
        data = {"title": "Python Updated"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 200
        assert response.json["title"] == "Python Updated"

    def test_departments_put_with_nonexistent_id(self):
        """
        Test put request with incorrect data (nonexistent department id).
        """
        wrong_id = 42
        data = {"title": "Python Updated"}
        response = self.client.put(f"/api/v1/departments/{wrong_id}", json=data)
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    def test_departments_put_with_id_wrong_data(self):
        """
        Test put request with incorrect data.
        """
        data = {"name": "Python+"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 400

    def test_departments_put_with_id_duplicate_name(self):
        """
        Test put request with incorrect data (duplicated title).
        """
        data = {"title": "C++"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 400
        assert "Department names should be unique" in response.json["message"]

    # Tests for DELETE requests
    def test_departments_delete_without_id(self):
        """
        Test delete request with incorrect data (not given id).
        """
        response = self.client.delete("/api/v1/departments")
        assert response.status_code == 405

    def test_departments_delete_with_id(self):
        """
        Test delete request with correct data.
        """
        response = self.client.delete("/api/v1/departments/1")
        assert response.status_code == 204
        assert len(response.data) == 0

    def test_departments_delete_with_nonexistent_id(self):
        """
        Test delete request with incorrect data (nonexistent department id).
        """
        wrong_id = 42
        response = self.client.delete(f"/api/v1/departments/{wrong_id}")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for DepartmentEmployeesAPI

    # Tests for GET requests
    def test_departments_employees_get_without_id(self):
        """
        Test get request.
        """
        response = self.client.get("/api/v1/departments/employees")
        assert response.status_code == 404

    def test_departments_employees_get_with_id(self):
        """
        Test get by id of department request.
        """
        dep_id = 1
        response = self.client.get(f"/api/v1/departments/{dep_id}/employees")
        assert response.status_code == 200
        assert all(emp["department"]["id_"] == dep_id for emp in response.json)

    def test_departments_employees_get_with_nonexistent_id(self):
        """
        Test get by invalid id of department request.
        """
        wrong_id = 42
        response = self.client.get(f"/api/v1/departments/{wrong_id}/employees")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for POST requests
    def test_departments_employees_post_without_id(self):
        """
        Test post request without id of department.
        """
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1999-01-01",
            "salary": 5000,
        }
        response = self.client.post("/api/v1/departments/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_post_with_id(self):
        """
        Test post request with department id.
        """
        dep_id = 1
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1995-05-05",
            "salary": 5000,
        }
        response = self.client.post(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 201
        assert response.json["department"]["id_"] == dep_id
        assert response.json["full_name"] == "New Employee"

    def test_departments_employees_post_with_nonexistent_id(self):
        """
        Test post request with incorrect data (nonexistent department id)..
        """
        wrong_id = 42
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1995-05-05",
            "salary": 5000,
        }
        response = self.client.post(f"/api/v1/departments/{wrong_id}/employees", json=data)
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    def test_departments_employees_post_with_id_wrong_data(self):
        """ Test post request with incorrect data."""
        dep_id = 1
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1995-05-05",
            "salary": -5000,
        }
        response = self.client.post(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 400

    # Tests for not allowed request methods
    def test_departments_employees_put(self):
        """ Test put request with incorrect data. (not given emp_id)"""
        dep_id = 1
        data = {
            "full_name": "New Employee updated",
            "date_of_birth": "1995-05-05",
            "salary": 5000,
        }
        response = self.client.put(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_patch(self):
        """ Test put request with part of data."""
        dep_id = 1
        data = {
            "full_name": "New Employee patched update",
        }
        response = self.client.patch(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_delete(self):
        """ Test delete request."""
        dep_id = 1
        response = self.client.delete(f"/api/v1/departments/{dep_id}/employees")
        assert response.status_code == 405
