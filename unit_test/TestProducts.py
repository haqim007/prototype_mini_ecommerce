import unittest
import json
import time

# local
from unit_test.BaseTestCase import BaseTestCase


class TestProductsBlueprint(BaseTestCase):
    """
    Test for Products blueprint
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

    def login_user(self, email, password):
        return self.client().post(
            '/auth/login',
            data=json.dumps(dict(
                email=email,
                password=password
            )),
            content_type='application/json',
        )

    def add_products(self, token, group_code, name, price, stocks, is_active):
        """
        Function to create/add new product
        """
        return self.client().post(
            '/product',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            data=json.dumps(dict(
                group_code=group_code,
                name=name,
                price=price,
                is_active=is_active,
                stocks=stocks
            )),
            content_type='application/json',
        )

    def test_add_product_with_valid_token(self):
        """
        Function to test add product for valid user/token
        """
        # Registration
        register = self.register_user(email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # add product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())

        self.assertEqual(add_product.status_code, 201)
        self.assertTrue(add_product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'success')
        self.assertTrue(data_product['message'] == 'Successfully added the product.')
        self.assertTrue(data_product['product'] is not None)

    def test_add_product_with_valid_token_but_not_admin(self):
        """
        Function to test add product for valid regular user not admin
        """
        # Registration
        register = self.register_user(email="user@mail.com", password="passsword123", is_admin=False)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("user@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # add product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())
        self.assertEqual(add_product.status_code, 401)
        self.assertTrue(add_product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'fail')
        self.assertTrue(data_product['message'] == 'Only admin can add product.')
        self.assertTrue(data_product['product'] is None)

    def test_add_product_with_invalid_token(self):
        """
        Function to test add product for invalid user/token
        """

        # add product
        add_product = self.add_products(
            token="randomstring", group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())
        self.assertEqual(add_product.status_code, 401)
        self.assertTrue(add_product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'fail')
        self.assertTrue(data_product['product'] is None)

    def test_add_product_without_token(self):
        """
        Function to test add product without token
        """
        # add product
        add_product = self.add_products(
            token="", group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())
        self.assertEqual(add_product.status_code, 403)
        self.assertTrue(add_product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'fail')
        self.assertTrue(data_product['product'] is None)

    # Get Products

    def get_product(self, token):
        """
        Function to get product
        """
        return self.client().get(
            '/product',
            headers=dict(
                Authorization='Bearer ' + token
            ),
            content_type='application/json',
        )

    def test_get_product_with_valid_token(self):
        """
        Function to test get product for valid user/token
        """
        # Registration
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # add 3 products
        count = 0
        while count < 3:
            add_product = self.add_products(
                token=data_login['auth_token'], group_code="1010",
                name="Bedak badak " + str(count), price=(10000 + count * 1000), stocks=1000, is_active=True)
            data_product = json.loads(add_product.data.decode())

            self.assertEqual(add_product.status_code, 201)
            self.assertTrue(add_product.content_type == 'application/json')
            self.assertTrue(data_product['status'] == 'success')
            self.assertTrue(data_product['message'] == 'Successfully added the product.')
            self.assertTrue(data_product['product'] is not None)
            count = count + 1

        product = self.get_product(data_login['auth_token'])
        data_product = json.loads(product.data.decode())
        # print(data_product)
        self.assertEqual(product.status_code, 200)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'success')
        self.assertTrue(data_product['message'] == 'Successfully retrieved products.')
        self.assertIsInstance(data_product['products'], list)
        self.assertTrue(len(data_product['products']) == 3)

    def test_get_product_with_valid_token_but_not_admin(self):
        """
        Function to test get product for valid regular user not admin
        """
        # Registration regular user
        register = self.register_user(
            email="user@mail.com", password="passsword123", is_admin=False)
        data_register = json.loads(register.data.decode())

        # Registration admin user
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register_admin = json.loads(register.data.decode())

        # login regular user
        login = self.login_user("user@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # login admin user
        login = self.login_user("admin@mail.com", "passsword123")
        data_login_admin = json.loads(login.data.decode())

        # add 3 products 2 active
        count = 0
        while count < 3:
            add_product = self.add_products(
                token=data_login_admin['auth_token'], group_code="1010",
                name=f"Bedak badak {count}", price=(10000 + count * 1000), stocks=1000, is_active=bool(count % 2 == 0))
            data_product = json.loads(add_product.data.decode())

            self.assertEqual(add_product.status_code, 201)
            self.assertTrue(add_product.content_type == 'application/json')
            self.assertTrue(data_product['status'] == 'success')
            self.assertTrue(data_product['message'] == 'Successfully added the product.')
            self.assertTrue(data_product['product'] is not None)
            count = count + 1

        product = self.get_product(data_login['auth_token'])
        data_product = json.loads(product.data.decode())

        self.assertEqual(product.status_code, 200)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'success')
        self.assertTrue(data_product['message'] == 'Successfully retrieved products.')
        self.assertIsInstance(data_product['products'], list)
        self.assertTrue(len(data_product['products']) == 2)

    def test_get_product_with_invalid_token(self):
        """
        Function to test get product for invalid user/token
        """

        # Registration admin user
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register_admin = json.loads(register.data.decode())

        # login admin user
        login = self.login_user("admin@mail.com", "passsword123")
        data_login_admin = json.loads(login.data.decode())

        # add 3 products 2 active
        count = 0
        while count < 3:
            add_product = self.add_products(
                token=data_login_admin['auth_token'], group_code="1010",
                name=f"Bedak badak {count}", price=(10000 + count * 1000), stocks=1000, is_active=bool(count % 2 == 0))
            data_product = json.loads(add_product.data.decode())

            self.assertEqual(add_product.status_code, 201)
            self.assertTrue(add_product.content_type == 'application/json')
            self.assertTrue(data_product['status'] == 'success')
            self.assertTrue(data_product['message'] == 'Successfully added the product.')
            self.assertTrue(data_product['product'] is not None)
            count = count + 1

        product = self.get_product("randomstring")
        data_product = json.loads(product.data.decode())

        self.assertEqual(product.status_code, 401)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'fail')
        self.assertIsInstance(data_product['products'], list)
        self.assertTrue(len(data_product['products']) == 0)

    def test_get_product_without_token(self):
        """
        Function to test get product without token
        """
        # Registration admin user
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register_admin = json.loads(register.data.decode())

        # login admin user
        login = self.login_user("admin@mail.com", "passsword123")
        data_login_admin = json.loads(login.data.decode())

        # add 3 products 2 active
        count = 0
        while count < 3:
            add_product = self.add_products(
                token=data_login_admin['auth_token'], group_code="1010",
                name=f"Bedak badak {count}", price=(10000 + count * 1000), stocks=1000, is_active=bool(count % 2 == 0))
            data_product = json.loads(add_product.data.decode())

            self.assertEqual(add_product.status_code, 201)
            self.assertTrue(add_product.content_type == 'application/json')
            self.assertTrue(data_product['status'] == 'success')
            self.assertTrue(data_product['message'] == 'Successfully added the product.')
            self.assertTrue(data_product['product'] is not None)
            count = count + 1

        product = self.get_product("")
        data_product = json.loads(product.data.decode())

        self.assertEqual(product.status_code, 403)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'fail')
        self.assertTrue(data_product['message'] == 'Provide a valid auth token.')
        self.assertIsInstance(data_product['products'], list)
        self.assertTrue(len(data_product['products']) == 0)


if __name__ == "__main__":
    unittest.main()
