"""This module contains class-based forms were done using wtf-forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Length


class DepartmentForm(FlaskForm):
    """
        Class creates form for accepting user data for department adding/editing.
        Provides data validation.
    """
    title = StringField(
        '',
        validators=[DataRequired('Name is required'), Length(min=3, max=128)],
        render_kw={'placeholder': 'Department name'}
    )
    submit = SubmitField('Save department')


class EmployeeForm(FlaskForm):
    """
        Class creates form for accepting user data for employee adding/editing.
        Provides data validation.
    """

    def __init__(self, departments, *args, **kwargs):
        """
        Initiate an EmployeeForm instance, accepts a positional argument 'departments'
        based on which generates the list of existing departments for select field.
        """
        super().__init__(*args, **kwargs)
        self.department_id.choices = [(dep['id_'], dep['title']) for dep in departments]

    full_name = StringField(
        '',
        validators=[DataRequired('Name is required'), Length(min=6, max=128)],
        render_kw={'placeholder': 'Employee name'}
    )

    date_of_birth = DateField("", [DataRequired("Please Enter your birthdate")])

    salary = IntegerField(
        '',
        validators=[DataRequired('Salary is required'),
                    NumberRange(min=0)],
        render_kw={'placeholder': 'Employee salary'}
    )

    department_id = SelectField('', validators=[DataRequired('Department id is required')])
    submit = SubmitField('Save employee')


class SearchEmployee(FlaskForm):
    """
        Class creates form for accepting user data for employees search.
        Provides data validation.
    """

    date_of_birth = DateField('', [DataRequired('Please Enter your birthdate')])
    date_for_interval = DateField('')
    submit = SubmitField('Find employees')
