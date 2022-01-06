# pylint: disable=R0401
"""
Module contains the definition of the blueprint for views.

Blueprints:
    department_views
    employee_views
"""
from flask import Blueprint

bp = Blueprint("views", __name__, template_folder="../templates")
from department_app.views import department_views, employee_views
