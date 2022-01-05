"""Module contains serializer schemas for Department and Employee classes."""
from marshmallow import fields, validate, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

import department_app.models as model
import department_app.service as ser


class DepartmentSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    department related data.
    """

    def get_avg_salary(self, obj):
        """Method to serialize the calculated average salary data on the fly."""
        return ser.DepartmentServices.get_avg_salary(obj)

    title = fields.String(required=True, error_messages={'message': 'title is required'},
                          validate=validate.Length(min=3, max=128))
    employees = fields.List(fields.Nested('EmployeeSchema', exclude=['department']), dump_only=True)
    avg_salary = fields.Method('get_avg_salary')

    class Meta:
        model = model.Department


class EmployeeSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow-SQLAlchemy schema for serializing/deserializing
    employee related data.
    """
    @staticmethod
    def validate_full_name(full_name: str):
        if not full_name.replace(" ", "").isalpha() or len(full_name.split()) != 2:
            raise ValidationError('Wrong full name')

    full_name = fields.String(required=True, error_messages={'required': 'full name is required'},
                              validate=[validate_full_name, validate.Length(min=6, max=128)])
    salary = fields.Integer(required=True, error_messages={'required': 'salary is required'},
                            validate=validate.Range(min=0))
    department_id = fields.Integer(required=True, error_messages={'required': 'department_id is required'},
                                   load_only=True)
    department = fields.Nested('DepartmentSchema', exclude=['employees'], dump_only=True)

    class Meta:
        model = model.Employee
