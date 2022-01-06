"""In this module custom error handlers are specified for 404 and 500 errors."""
from flask import render_template, current_app as app

from department_app.errors import bp


@bp.app_errorhandler(404)
def page_not_found(exception):
    """A handler that is called when a 404(not found) error occurs"""
    app.logger.error(exception)
    return render_template("error_404.html", description=exception.description), 404


@bp.app_errorhandler(500)
def server_error(exception):
    """A handler that is called when a 500(internal server error) error occurs"""
    app.logger.error(exception)
    return render_template("error_500.html", description=exception.description), 500
