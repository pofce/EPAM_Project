# pylint: disable=C0415
"""
Module containing factory for app merging it with database, blueprints, REST.

Functions:
    create_app()
"""
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from config import Config
from department_app.models import db

migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    """
    Function to create a Flask application instance with provided configuration.
    In the function the extensions are initialized with the app instance, the errors
       and views blueprints are registered.
    :return: Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    with app.app_context():
        from .rest import api

        api.init_app(app)
        from department_app.views import bp as views_bp

        app.register_blueprint(views_bp)
        from department_app.errors import bp as errors_bp

        app.register_blueprint(errors_bp)

        # Create log folder if to doesn't exist
    if not app.debug and not app.testing:
        if not os.path.exists("log"):
            os.mkdir("log")

        # Create handler and set level to debug
        file_handler = RotatingFileHandler(
            "log/app.log", maxBytes=10240, backupCount=5
        )

        # Set the Formatter
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.DEBUG)

        app.logger.setLevel(logging.DEBUG)
        # Add handlers to the logger
        app.logger.addHandler(file_handler)

    return app
