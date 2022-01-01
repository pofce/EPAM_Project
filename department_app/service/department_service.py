"""" Module contains Department Service class with methods for DB CRUD operations."""
from department_app.models import db, Department


class DepartmentServices:
    """Class with methods for DB CRUD operation on departments."""

    @staticmethod
    def get_all():
        """
        get_all returns a list with all Department objects from the DB.
        """
        return Department.query.all()

    @staticmethod
    def get_by_id(dep_id):
        """
        Get a specific department by id from DB.
        :param dep_id: Id of the department to fetch (int)
        :return: Department with id=dep_id, None if no such department.
        """
        return Department.query.filter_by(id_=dep_id).first()

    @staticmethod
    def create(data):
        """
        Create a new Department instance from dict and save new entry to DB
        :param data: A dict with data to create a department from.
        :return: the created instance
        """
        department = Department(**data)
        db.session.add(department)
        db.session.commit()
        return department

    @staticmethod
    def update(department, data):
        """
        Update a Department object and related DB entry with data from dict.
        :param department: A Department instance.
        :param data: A dict with data to update the department with.
        :return: The updated instance.
        """
        for key in data:
            if key in department.__dict__.keys():
                department.__setattr__(key, data[key])
        db.session.commit()
        return department

    @staticmethod
    def delete(department):
        """
        Delete a Department instance and related data from DB
        :param department: The department to be deleted.
        :return: None
        """
        db.session.delete(department)
        db.session.commit()

    @staticmethod
    def get_avg_salary(department):
        """
        Calculate the average salary for employees in working department.
        :param department: A Department instance to calculate the average for.
        :return: The average salary round to 2 digits after point.
        0 if no employees in the department.
        """
        if not list(department.employees):
            return 0
        return round(sum(employee.salary for employee in department.employees) / len(list(department.employees)))
