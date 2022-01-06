"""Module contains classes to store configurations"""


class Config:
    """Main configuration"""
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:dkfl007@localhost/project_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "big_secret"


class TestConfig(Config):
    """Configuration for testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
