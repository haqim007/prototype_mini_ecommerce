import unittest
import json
import time

# local
from models.UserModel import User
from unit_test.BaseTestCase import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    """
    Test blueprint auth
    """

    def register_user(self, email, password, is_admin=False):
        """
        Function to hit end-point of registration
        """
        return self.client().post(
            '/auth/register',
            data=json.dumps(dict(
                email=email,
                password=password,
                is_admin=is_admin
            )),
            content_type='application/json',
        )

    def test_registration(self):
        """
        Test for user registration
        """

        with self.client():
            res = self.register_user("admin@mail.com", "123456")

            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])

    def test_registration_for_registered_user(self):
        """
        Test registration for registered email
        """
        with self.app.app_context():
            # first registration
            res = self.register_user("admin@mail.com", "123456")
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])

            # direct insert into db
            # user = User(
            #     email="admin@mail.com",
            #     password="password1234"
            # )
            # user.save()

            # second registeration
            res = self.register_user("admin@mail.com", "password")
            data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 202)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Login.')

    def login_user(self, email, password):
        return self.client().post(
            '/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def test_login_for_registered_user(self):
        """
            Test login for registered user
        """

        with self.client():
            # register a user
            res = self.register_user("admin@mail.com", "123456", True)
            data_register = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])

            # login
            res = self.login_user("admin@mail.com", "123456")
            data_login = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])

    def test_login_for_not_registered_user(self):
        """
            Test login for not registered user
        """

        with self.client():
            # login
            res = self.login_user("admin@mail.com", "123456")
            data_login = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 404)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_login['status'] == 'fail')
            self.assertTrue(data_login['message'] == 'User does not exist.')

    def logout_user(self, token):

        res = self.client().post(
            '/auth/logout',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            content_type='application/json',
        )

        return res

    def test_logout_for_logged_in_user(self):
        """
        Test logout for logged in user
        """
        with self.client():
            # user registration
            res = self.register_user("admin@mail.com", "123456", True)
            data_register = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])

            # login
            res = self.login_user("admin@mail.com", "123456")
            data_login = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])

            # logout
            res = self.logout_user(data_login['auth_token'])
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(res.status_code, 200)

    def test_logout_for_expired_logged_in_user(self):
        """
        Test logout for expired login user
        """
        with self.app.app_context():
            # user registration
            res = self.register_user("admin@mail.com", "123456", True)
            data_register = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 201)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(data_register['message'] == 'Successfully registered.')
            self.assertTrue(data_register['auth_token'])

            # login
            res = self.login_user("admin@mail.com", "123456")
            data_login = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 200)
            self.assertTrue(res.content_type == 'application/json')
            self.assertTrue(data_login['status'] == 'success')
            self.assertTrue(data_login['message'] == 'Successfully logged in.')
            self.assertTrue(data_login['auth_token'])
            # invalid token logout
            time.sleep(6)
            res = self.logout_user(data_login['auth_token'])
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'fail')
            # self.assertTrue(data['message'] == 'Signature expired. Please login')
            self.assertEqual(res.status_code, 401)

    def test_logout_without_token(self):
        """
        Test logout without token
        """
        with self.client():

            # invalid token logout
            res = self.logout_user("")
            data = json.loads(res.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(res.status_code, 403)

    def test_logout_using_blacklisted_token(self):
        """
        Test logout by using blacklisted_token. In case user login from more than one devices
        """
        # user registration
        res = self.register_user("admin@mail.com", "123456", True)
        data_register = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.content_type == 'application/json')
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['message'] == 'Successfully registered.')
        self.assertTrue(data_register['auth_token'])

        # login
        res = self.login_user("admin@mail.com", "123456")
        data_login = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.content_type == 'application/json')
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['auth_token'])

        # logout
        res = self.logout_user(data_login['auth_token'])
        data = json.loads(res.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(res.status_code, 200)

        # logout second time
        res = self.logout_user(data_login['auth_token'])
        data = json.loads(res.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
