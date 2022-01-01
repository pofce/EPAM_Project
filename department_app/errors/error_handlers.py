from flask import render_template, current_app as app

from department_app.errors import bp


@bp.app_errorhandler(404)
def page_not_found(e):
    """A handler that is called when a 404(not found) error occurs"""
    app.logger.error(e)
    return render_template("error_404.html", description=e.description), 404


@bp.app_errorhandler(500)
def server_error(e):
    """A handler that is called when a 500(internal server error) error occurs"""
    app.logger.error(e)
    return render_template("error_500.html", description=e.description), 500
