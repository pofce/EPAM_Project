"""" Module contains Employee Service class with methods for DB CRUD operations."""
from department_app.models import db, Employee


class EmployeeServices:
    """Class with methods for DB CRUD operation on employees."""

    @staticmethod
    def get_all():
        """
        get_all returns a list with all Employee objects from the DB.
        """
        return Employee.query.all()

    @staticmethod
    def get_all_from_department(dep_id):
        """
        Get all employees working in a specified departmentю
        :param dep_id: ID of the department(int)
        :return: A list with all Employee instances with "department_id=dep_id"
        Or an empty list if no employees in department with id=dep_id.
        """
        return Employee.query.filter_by(department_id=dep_id).all()

    @staticmethod
    def get_by_id(emp_id):
        """
        Get a specific employee by id from DB.
        :param emp_id: Id of the employee to fetch (int)
        :return: Employee with id=dep_id, None if no such department.
        """
        return Employee.query.filter_by(id_=emp_id).first()

    @staticmethod
    def get_by_date_of_birth(date, date_for_interval=None):
        """
        Get employees born on a specific date or in an interval between dates.
        :param date: date object to get employees born on specific date
        or lower point for interval to get employees born in interval
        (if date_for_interval passed).
        :param date_for_interval: date object to specify the upper point
        for interval to get employees born in interval.
        :return: a list of employees with date_of_birth matching the provided
        parameters. Empty list if no matches.
        """
        if date_for_interval is None:
            return Employee.query.filter_by(date_of_birth=date).all()
        return Employee.query.filter(date <= Employee.date_of_birth, Employee.date_of_birth <= date_for_interval).all()

    @staticmethod
    def get_by_date_of_birth_from_department(dep_id, date, date_for_interval=None):
        """
        Get employees born on a specific date or in an interval between dates,
        who work in a specified department.
        :param dep_id: Id of the department to get employees from (int).
        :param date: date object to get employees born on specific date
        or lower point for interval to get employees born in interval
        (if date_for_interval passed).
        :param date_for_interval: date object to specify the upper point
        for interval to get employees born in interval.
        :return: a list of employees with date_of_birth matching the provided
        parameters. Empty list if no matches.
        """
        if date_for_interval is None:
            return Employee.query.filter_by(date_of_birth=date).filter_by(department_id=dep_id).all()
        return Employee.query.filter(
            date <= Employee.date_of_birth, Employee.date_of_birth <= date_for_interval
        ).filter_by(department_id=dep_id).all()

    @staticmethod
    def create(data):
        """
        Create a new Employee instance from dict and save new entry to DB
        :param data: A dict with data to create an employee from.
        :return: the created instance
        """
        employee = Employee(**data)
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def update(employee, data):
        """
        Update an Employee object and related DB entry with data from dict.
        :param employee: An Employee instance to be updated.
        :param data: A dict with data to update the employee with.
        :return: The updated instance.
        """
        for key in data:
            if key in employee.__dict__.keys():
                employee.__setattr__(key, data[key])
        db.session.commit()
        return employee

    @staticmethod
    def delete(employee):
        """
        Delete an Employee instance and related data from DB
        :param employee: The employee to be deleted.
        :return: None
        """
        db.session.delete(employee)
        db.session.commit()
