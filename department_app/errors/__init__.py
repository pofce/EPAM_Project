"""Module contains the definition of the blueprint for error-handlers."""
from flask import Blueprint

bp = Blueprint("errors", __name__, template_folder="../templates")
from department_app.errors import error_handlers
