"""
Module defines department and employee models using class Model from SQLAlchemy
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    """Department class defines a database table for departments"""

    __tablename__ = 'departments'
    id_: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(128), unique=True, nullable=False)
    employees = db.relationship('Employee', backref=db.backref('department'), cascade="all,delete", lazy='dynamic')


class Employee(db.Model):
    """Employee class defines a database table for employees"""

    __tablename__ = 'employees'
    id_: int = db.Column(db.Integer, primary_key=True)
    full_name: str = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False, index=True)
    salary: int = db.Column(db.Integer, nullable=False, index=True)
    department_id: int = db.Column(db.Integer, db.ForeignKey('departments.id_'), nullable=False)

