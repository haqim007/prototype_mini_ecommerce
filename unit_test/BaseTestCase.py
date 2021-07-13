# from flask_testing import TestCase
import unittest
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """ Parent of all test units """

    def setUp(self):
        """ Define test variables and init app """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        # bind the app to current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables after running a function of test."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
