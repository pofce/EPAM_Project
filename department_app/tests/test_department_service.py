from department_app.service import DepartmentServices, EmployeeServices
from ..tests.conftest import BaseTestCase


class TestDepartmentService(BaseTestCase):
    """
    This is the class for department service test cases
    """

    def test_get_all(self):
        """
        Test get all departments operation
        """
        departments = DepartmentServices.get_all()
        assert len(departments) == 3

    def test_get_by_id(self):
        """
        Test get department by id operation
        """
        department = DepartmentServices.get_by_id(1)
        assert department is not None
        assert department.title == "Python"

    def test_get_by_wrong_id(self):
        """
        Test get not existing department by id operation.
        """
        department = DepartmentServices.get_by_id(42)
        assert department is None

    def test_create(self):
        """
        Test create department operation.
        """
        department = DepartmentServices.create(dict(title="PHP"))
        departments = DepartmentServices.get_all()
        assert department.title == "PHP"
        assert len(departments) == 4
        assert department in departments

    def test_create_wrong_data(self):
        """
        Test create department operation with wrong data.
        """
        with self.assertRaises(TypeError) as context:
            DepartmentServices.create(dict(name="Fail"))

    def test_update(self):
        """
        Test update department operation.
        """
        department_to_update = DepartmentServices.get_by_id(1)
        updated = DepartmentServices.update(
            department_to_update, dict(title="Updated Python")
        )
        departments = DepartmentServices.get_all()
        assert updated.title == "Updated Python"
        assert len(departments) == 3

    def test_delete(self):
        """
        Test delete department operation.
        """
        department_to_delete = DepartmentServices.get_by_id(1)
        DepartmentServices.delete(department_to_delete)
        departments = DepartmentServices.get_all()
        employees = EmployeeServices.get_all()
        assert department_to_delete not in departments
        assert len(departments) == 2
        # to check if cascade delete happened
        assert len(employees) == 6

    def test_avg_salary_non_empty_departments(self):
        """
        Test get average salary operation from non-empty department.
        """
        dep_1 = DepartmentServices.get_by_id(1)
        dep_2 = DepartmentServices.get_by_id(2)
        salary_1 = DepartmentServices.get_avg_salary(dep_1)
        salary_2 = DepartmentServices.get_avg_salary(dep_2)
        assert salary_1 == 1375
        assert salary_2 == 2000

    def test_avg_salary_empty_department(self):
        """
        Test get average salary operation from empty department.
        """
        dep_4 = DepartmentServices.create(dict(title="PHP"))
        salary_4 = DepartmentServices.get_avg_salary(dep_4)
        assert salary_4 == 0
