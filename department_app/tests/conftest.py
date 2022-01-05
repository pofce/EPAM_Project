"""
This module defines the BaseTestCase class
"""
import unittest

from department_app import create_app, db
from department_app.models.population import populate_bd
from config import TestConfig


class BaseTestCase(unittest.TestCase):
    """
    Base test case class
    """
    def setUp(self):
        """
        Execute before every test case
        """
        self.app = create_app(config_class=TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        populate_bd()
        self.client = self.app.test_client()

    def tearDown(self):
        """
        Execute after every test case
        """
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
