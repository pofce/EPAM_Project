# pylint: disable=R0903
"""Module contains serializer schemas for Department and Employee classes."""
from marshmallow import fields, validate, ValidationError, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import department_app.models as model
import department_app.service as ser


class DepartmentSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    department related data.
    """
    @staticmethod
    def get_avg_salary(obj):
        """Method to serialize the calculated average salary data on the fly."""
        return ser.DepartmentServices.get_avg_salary(obj)

    title = fields.String(required=True, error_messages={'message': 'title is required'},
                          validate=validate.Length(min=3, max=128))
    employees = fields.List(fields.Nested('EmployeeSchema', exclude=['department']), dump_only=True)
    avg_salary = fields.Method('get_avg_salary')

    class Meta:
        """Meta class"""
        model = model.Department


class EmployeeSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    employee related data.
    """

    full_name = fields.String(required=True, error_messages={'required': 'full name is required',
                                                             'validate_full_name': 'Wrong full name'},
                              validate=[validate.Length(min=6, max=128)])

    @validates('full_name')
    def validate_full_name(self, full_name: str):
        """Method checks if entered full_name is correct on the fly."""
        if not full_name.replace(" ", "").isalpha() or len(full_name.split()) != 2:
            raise ValidationError('Wrong full name')

    salary = fields.Integer(required=True, error_messages={'required': 'salary is required'},
                            validate=validate.Range(min=0))
    department_id = fields.Integer(required=True,
                                   error_messages={'required': 'department_id is required'},
                                   load_only=True)
    department = fields.Nested('DepartmentSchema', exclude=['employees'], dump_only=True)

    class Meta:
        """Meta class"""
        model = model.Employee
