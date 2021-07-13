import unittest
import json

# local
from models.UserModel import User
from unit_test.BaseTestCase import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):

        # bind the app to current context
        with self.app.app_context():
            user = User(
                email="admin@mail.com",
                password="password123",
            )
            user.save()
            auth_token = user.encode_auth_token(user.id)
            self.assertIsInstance(auth_token, str)

    def test_decode_auth_token(self):

        # bind the app to current context
        with self.app.app_context():
            user = User(
                email="admin@mail.com",
                password="password1234"
            )
            user.save()
            auth_token = user.encode_auth_token(user.id)
            self.assertIsInstance(auth_token, str)
            self.assertIsInstance(User.decode_auth_token(auth_token), int)
            self.assertTrue(User.decode_auth_token(auth_token) == 1)


# make this file executable
if __name__ == "__main__":
    unittest.main()
