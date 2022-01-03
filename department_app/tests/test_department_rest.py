"""
Module contains class to test department api.
"""
import json
from distutils.version import LooseVersion


from department_app.tests.conftest import BaseTestCase, create_app


class TestDepartmentApi(BaseTestCase):
    """
    Class for department api test cases.
    """

    client = create_app().test_client()

    # Tests for GET requests
    def test_departments_get_all(self):
        response = self.client.get("/api/v1/departments")
        assert response.status_code == 200
        assert len(response.json) == 3

    def test_departments_get_with_id(self):
        response = self.client.get("/api/v1/departments/1")
        assert response.status_code == 200
        assert response.json["title"] == "Python"

    def test_departments_get_with_nonexistent_id(self):
        wrong_id = 42
        response = self.client.get(f"/api/v1/departments/{wrong_id}")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for POST requests
    def test_departments_post(self):
        data = {"title": "PHP"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 201
        assert response.json["title"] == "PHP"

    def test_departments_post_wrong_data(self):
        data = {"name": "PHP"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 400

    def test_departments_post_duplicate_name(self):
        data = {"title": "Python"}
        response = self.client.post("/api/v1/departments", json=data)
        assert response.status_code == 400
        assert "Department names should be unique" in response.json["message"]

    def test_departments_post_with_id(self):
        data = {"title": "Css"}
        response = self.client.post("/api/v1/departments/1", json=data)
        assert response.status_code == 405

    # Tests for PUT requests
    def test_departments_put_without_id(self):
        data = {"title": "Python+"}
        response = self.client.put("/api/v1/departments/", json=data)
        assert response.status_code == 405

    def test_departments_put_with_id(self):
        data = {"title": "Python Updated"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 200
        assert response.json["title"] == "Python Updated"

    def test_departments_put_with_nonexistent_id(self):
        wrong_id = 42
        data = {"title": "Python Updated"}
        response = self.client.put(f"/api/v1/departments/{wrong_id}", json=data)
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    def test_departments_put_with_id_wrong_data(self):
        data = {"name": "Python+"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 400

    def test_departments_put_with_id_duplicate_name(self):
        data = {"title": "C++"}
        response = self.client.put("/api/v1/departments/1", json=data)
        assert response.status_code == 400
        assert "Department names should be unique" in response.json["message"]

    # Tests for DELETE requests
    def test_departments_delete_without_id(self):
        response = self.client.delete("/api/v1/departments")
        assert response.status_code == 405

    def test_departments_delete_with_id(self):
        response = self.client.delete("/api/v1/departments/1")
        assert response.status_code == 204
        assert len(response.data) == 0

    def test_departments_delete_with_nonexistent_id(self):
        wrong_id = 42
        response = self.client.delete(f"/api/v1/departments/{wrong_id}")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for DepartmentEmployeesAPI

    # Tests for GET requests
    def test_departments_employees_get_without_id(self):
        response = self.client.get("/api/v1/departments/employees")
        assert response.status_code == 404

    def test_departments_employees_get_with_id(self):
        dep_id = 1
        response = self.client.get(f"/api/v1/departments/{dep_id}/employees")
        assert response.status_code == 200
        assert all(emp["department"]["id_"] == dep_id for emp in response.json)

    def test_departments_employees_get_with_nonexistent_id(self):
        wrong_id = 42
        response = self.client.get(f"/api/v1/departments/{wrong_id}/employees")
        assert response.status_code == 404
        assert f"Department with id = {wrong_id} was not found" in response.json["message"]

    # Tests for POST requests
    def test_departments_employees_post_without_id(self):
        data = {
            "full_name": "New Employee",
            "date_of_birth": "1999-01-01",
            "salary": 5000,
        }
        response = self.client.post("/api/v1/departments/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_post_with_id(self):
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
        dep_id = 1
        data = {
            "full_name": "New Employee updated",
            "date_of_birth": "1995-05-05",
            "salary": 5000,
        }
        response = self.client.put(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_patch(self):
        dep_id = 1
        data = {
            "full_name": "New Employee patched update",
        }
        response = self.client.patch(f"/api/v1/departments/{dep_id}/employees", json=data)
        assert response.status_code == 405

    def test_departments_employees_delete(self):
        dep_id = 1
        response = self.client.delete(f"/api/v1/departments/{dep_id}/employees")
        assert response.status_code == 405
