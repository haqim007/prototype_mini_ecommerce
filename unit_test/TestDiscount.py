import unittest
import json
from datetime import datetime, timedelta

# local
from unit_test.BaseTestCase import BaseTestCase


class TestDiscountBlueprint(BaseTestCase):
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

    # def create_discount(self, token, )

    @staticmethod
    def myconverter(o):
        if isinstance(o, datetime):
            return o.__str__()

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

    def test_create_discount(self):
        """
        Function to test create new discount
        """

        # Registration
        register = self.register_user(email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())

        discount = self.client().post(
            '/discount',
            headers=dict(
                Authorization='Bearer ' + data_login['auth_token']
            ),
            data=json.dumps(dict(
                name="flash sale bedak",
                rate=0.1,
                start_campaign_datetime=datetime.strptime('12/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                end_campaign_datetime=datetime.strptime('13/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                product_id=data_product['product']['id']
            ), default=self.myconverter),
            content_type='application/json',
        )
        data_discount = json.loads(discount.data.decode())

        self.assertEqual(discount.status_code, 201)
        self.assertTrue(discount.content_type == 'application/json')
        self.assertTrue(data_discount['status'] == 'success')
        self.assertTrue(data_discount['message'] == 'Successfully added the discount.')
        self.assertTrue(data_discount['discount'] is not None)

        product = self.get_product(data_login['auth_token'])
        data_product = json.loads(product.data.decode())
        print(data_product)
        self.assertEqual(product.status_code, 200)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'success')
        self.assertTrue(data_product['message'] ==
                        'Successfully retrieved products.')
        self.assertIsInstance(data_product['products'], list)

    def test_create_discount_not_admin(self):
        """
        Function to test create new discount using not admin account
        """

        # Registration
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # Registration not admin
        register = self.register_user(
            email="user@mail.com", password="passsword123", is_admin=False)
        data_register_user = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # login not admin
        login = self.login_user("user@mail.com", "passsword123")
        data_login_user = json.loads(login.data.decode())

        # product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())

        discount = self.client().post(
            '/discount',
            headers=dict(
                Authorization='Bearer ' + data_login_user['auth_token']
            ),
            data=json.dumps(dict(
                name="flash sale bedak",
                rate=0.1,
                start_campaign_datetime=datetime.strptime(
                    '12/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                end_campaign_datetime=datetime.strptime(
                    '13/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                product_id=data_product['product']['id']
            ), default=self.myconverter),
            content_type='application/json',
        )
        data_discount = json.loads(discount.data.decode())

        self.assertEqual(discount.status_code, 401)
        self.assertTrue(discount.content_type == 'application/json')
        self.assertTrue(data_discount['status'] == 'fail')
        self.assertTrue(data_discount['message'] == 'Only admin can add discount.')
        self.assertTrue(data_discount['discount'] is None)

    def test_create_discount_without_token(self):
        """
        Function to test create new discount without token
        """

        # Registration
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())

        discount = self.client().post(
            '/discount',
            headers=dict(
                Authorization='Bearer ' + ""
            ),
            data=json.dumps(dict(
                name="flash sale bedak",
                rate=0.1,
                start_campaign_datetime=datetime.strptime(
                    '12/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                end_campaign_datetime=datetime.strptime(
                    '13/07/2021 01:55:19', "%d/%m/%Y %H:%M:%S"),
                product_id=data_product['product']['id']
            ), default=self.myconverter),
            content_type='application/json',
        )
        data_discount = json.loads(discount.data.decode())

        self.assertEqual(discount.status_code, 403)
        self.assertTrue(discount.content_type == 'application/json')
        self.assertTrue(data_discount['status'] == 'fail')
        self.assertTrue(data_discount['message'] == 'Provide a valid auth token.')
        self.assertTrue(data_discount['discount'] is None)

    def test_create_discount_not_in_period_discount(self):
        """
        Function to test create new discount
        """

        # Registration
        register = self.register_user(
            email="admin@mail.com", password="passsword123", is_admin=True)
        data_register = json.loads(register.data.decode())

        # login
        login = self.login_user("admin@mail.com", "passsword123")
        data_login = json.loads(login.data.decode())

        # product
        add_product = self.add_products(
            token=data_login['auth_token'], group_code="1010",
            name="Bedak badak", price=10000, stocks=1000, is_active=True)
        data_product = json.loads(add_product.data.decode())

        discount = self.client().post(
            '/discount',
            headers=dict(
                Authorization='Bearer ' + data_login['auth_token']
            ),
            data=json.dumps(dict(
                name="flash sale bedak",
                rate=0.2,
                start_campaign_datetime=datetime.now() + timedelta(days=1),
                end_campaign_datetime=datetime.now() + timedelta(days=2),
                product_id=data_product['product']['id']
            ), default=self.myconverter),
            content_type='application/json',
        )
        data_discount = json.loads(discount.data.decode())
        self.assertEqual(discount.status_code, 201)
        self.assertTrue(discount.content_type == 'application/json')
        self.assertTrue(data_discount['status'] == 'success')
        self.assertTrue(data_discount['message'] == 'Successfully added the discount.')
        self.assertTrue(data_discount['discount'] is not None)

        product = self.get_product(data_login['auth_token'])
        data_product = json.loads(product.data.decode())

        self.assertEqual(product.status_code, 200)
        self.assertTrue(product.content_type == 'application/json')
        self.assertTrue(data_product['status'] == 'success')
        self.assertTrue(data_product['message'] == 'Successfully retrieved products.')
        self.assertIsInstance(data_product['products'], list)
        self.assertTrue(data_product['products'][0]['discount'] is None)


if __name__ == "__main__":
    unittest.main()
