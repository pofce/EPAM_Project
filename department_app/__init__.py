"""
Module containing factory for app merging it with database, blueprints, REST.

Functions:
    create_app()
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

import department_app.models as model
from config import TestConfig

migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=TestConfig):
    """
    Function to create a Flask application instance with provided configuration.
    In the function the extensions are initialized with the app instance, the errors
       and views blueprints are registered.
    :return: Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    model.db.init_app(app)
    migrate.init_app(app, model.db)
    bootstrap.init_app(app)
    with app.app_context():
        from .rest import api

        api.init_app(app)
        from department_app.views import bp as views_bp

        app.register_blueprint(views_bp)
        from department_app.errors import bp as errors_bp

        app.register_blueprint(errors_bp)
    return app
