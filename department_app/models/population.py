"""Module contains a function to populate test data in database."""
from datetime import date
from department_app import create_app
from department_app.models import Department, Employee, db


def populate_bd():
    """
       Initialises and populates database with departments and employees.
    """

    dep1 = Department(title='Python')
    dep2 = Department(title='C++')
    dep3 = Department(title='Assembler')

    e_1 = Employee(
        full_name="Vladyslav Radchenko",
        date_of_birth=date(year=2002, month=9, day=9),
        salary=1500,
        department_id=1,
    )

    e_2 = Employee(
        full_name="Rhian Sutherland",
        date_of_birth=date(year=1992, month=2, day=2),
        salary=1000,
        department_id=1,
    )

    e_3 = Employee(
        full_name="Dillan Dejesus",
        date_of_birth=date(year=1973, month=3, day=3),
        salary=2000,
        department_id=2,
    )

    e_4 = Employee(
        full_name="Evie Amin",
        date_of_birth=date(year=1995, month=4, day=4),
        salary=2000,
        department_id=2,
    )

    e_5 = Employee(
        full_name="Neil Wilson",
        date_of_birth=date(year=1985, month=5, day=5),
        salary=2000,
        department_id=2,
    )

    e_6 = Employee(
        full_name="Ayah Hobbs",
        date_of_birth=date(year=1981, month=1, day=1),
        salary=1000,
        department_id=1,
    )

    e_7 = Employee(
        full_name="Corban Snow",
        date_of_birth=date(year=1962, month=2, day=2),
        salary=1000,
        department_id=3,
    )

    e_8 = Employee(
        full_name="Carmel Boyle",
        date_of_birth=date(year=1983, month=3, day=3),
        salary=2000,
        department_id=3,
    )

    e_9 = Employee(
        full_name="Reema Hoover",
        date_of_birth=date(year=1999, month=4, day=4),
        salary=2000,
        department_id=1,
    )

    e_10 = Employee(
        full_name="Abdirahman Davidson",
        date_of_birth=date(year=1995, month=5, day=5),
        salary=2000,
        department_id=2,
    )

    all_data = (dep1, dep2, dep3, e_1, e_2, e_3, e_4, e_5, e_6, e_7, e_8, e_9, e_10)

    for data in all_data:
        db.session.add(data)
    db.session.commit()
    db.session.close()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_bd()
