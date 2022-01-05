from department_app.service import EmployeeServices
from ..tests.conftest import BaseTestCase

from datetime import date
from sqlalchemy.exc import IntegrityError


class TestDepartmentService(BaseTestCase):
    """
    This is the class for department service test cases
    """
    def test_get_all(self):
        """
        Test get all employees operation
        """
        employees = EmployeeServices.get_all()
        assert len(employees) == 10

    def test_get_from_department(self):
        """
        Test get all employees from department operation
        """
        dep_1_employees = EmployeeServices.get_all_from_department(1)
        dep_2_employees = EmployeeServices.get_all_from_department(2)
        dep_3_employees = EmployeeServices.get_all_from_department(5)
        assert len(dep_1_employees) == 4
        assert len(dep_2_employees) == 4
        assert len(dep_3_employees) == 0

    def test_get_by_valid_id(self):
        """
        Test get all employee by id operation
        """
        emp_1 = EmployeeServices.get_by_id(1)
        assert emp_1 is not None
        assert emp_1.full_name == "Vladyslav Radchenko"

    def test_get_by_invalid_id(self):
        """
        Test get all employee by invalid id operation
        """
        emp_42 = EmployeeServices.get_by_id(42)
        assert emp_42 is None

    def test_create(self):
        """
        Test create employee operation.
        """
        new_employee = EmployeeServices.create(
            dict(
                full_name="New Employee",
                date_of_birth=date(1999, 9, 9),
                salary=999,
                department_id=1,
            )
        )
        employees = EmployeeServices.get_all()
        assert new_employee.full_name == "New Employee"
        assert len(employees) == 11
        assert new_employee in employees

    def test_create_incomplete_data(self):
        """
        Test create employee operation with lack of required data.
        """
        with self.assertRaises(IntegrityError):
            EmployeeServices.create(
                dict(
                    full_name="New Employee",
                    salary=3000,
                    department_id=1,
                )
            )

    def test_update(self):
        """
        Test update employee operation.
        """
        employee_to_update = EmployeeServices.get_by_id(1)
        updated = EmployeeServices.update(
            employee_to_update,
            dict(
                full_name="Updated Employee",
                department_id=2,
            ),
        )
        employees = EmployeeServices.get_all()
        assert updated.full_name == "Updated Employee"
        assert updated.department_id == 2
        assert updated.salary == employee_to_update.salary
        assert len(employees) == 10
        assert updated in employees

    def test_delete(self):
        """
        Test delete employee operation.
        """
        employee_to_delete = EmployeeServices.get_by_id(1)
        EmployeeServices.delete(employee_to_delete)
        employees = EmployeeServices.get_all()
        assert employee_to_delete not in employees
        assert len(employees) == 9

    def test_get_by_date_of_birth_without_interval(self):
        """
        Test get employees by date of birth operation.
        """
        test_date = date(1991, 1, 1)
        employees = EmployeeServices.get_by_date_of_birth(test_date)
        assert all(emp.date_of_birth == test_date for emp in employees)

    def test_get_by_date_of_birth_with_interval(self):
        """
        Test get employees operation which takes all who were born in specific interval.
        """
        test_date1 = date(1991, 1, 1)
        test_date2 = date(1993, 3, 3)
        employees = EmployeeServices.get_by_date_of_birth(test_date1, test_date2)
        assert all(test_date1 <= emp.date_of_birth <= test_date2 for emp in employees)

    def test_get_by_date_of_birth_from_department_without_interval(self):
        """
        Test get employees by date of birth and department id operation.
        """
        dep_id = 1
        test_date = date(1991, 1, 1)
        employees = EmployeeServices.get_by_date_of_birth_from_department(dep_id, test_date)
        assert all(emp.date_of_birth == test_date for emp in employees)
        assert all(emp.department_id == dep_id for emp in employees)

    def test_get_by_date_of_birth_from_department_with_interval(self):
        """
        Test get employees operation which takes all who belong to specific department and were born in interval.
        """
        dep_id = 1
        test_date1 = date(1991, 1, 1)
        test_date2 = date(2000, 1, 1)
        employees = EmployeeServices.get_by_date_of_birth_from_department(
            dep_id, test_date1, test_date2
        )
        assert all(test_date1 <= emp.date_of_birth <= test_date2 for emp in employees)
        assert all(emp.department_id == dep_id for emp in employees)

