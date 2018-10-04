"""tests for orders.py file"""
import unittest
import json

# local imports
from app import create_app
from app.api.v2.datamodels import drop_tables


class TestBase(unittest.TestCase):
    """Base class for all tests"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.header_no_token = {'content-type': 'application/json'}
        self.sample_registration_data = {
            "name": "Admin",
            "email": "admin@app.com",
            "password": "password",
            "confirm_password": "password"
        }
        self.sample_login_data = {
            "name": "Admin",
            "password": "password"
        }

        self.sample_menu_data = {
            "name": "Pizza",
            "description": "New Pizza in town",
            "price": 200
        }
        self.sample_order_without_quantity = {
            "name": "Pizza",
            "address": "Nairobi "
        }

        self.sample_invalid_status = {
            "status": "am_wrong"
        }

        # register admin user
        self.registration_response = self.registration_helper(
            self.sample_registration_data)

        self.token = self.login_helper(self.sample_login_data)
        self.admin_header = {'content-type': 'application/json',
                             'x-access-token': self.token}

    def registration_helper(self, registration_data):
        '''Helper method to register a user'''

        response = self.client.post(
            '/api/v2/auth/users',
            data=json.dumps(registration_data),
            headers=self.header_no_token)
        return response

    def login_helper(self, login_data):
        '''login helper funnction'''
        test_response = self.client.post(
            '/api/v2/auth/login',
            data=json.dumps(login_data),
            headers=self.header_no_token)
        response_data = json.loads(test_response.data.decode('utf-8'))['token']
        return response_data

    def promote_user_helper(self):
        '''promote'''
        response = self.client.put(
            '/api/v2/promote/1',
            headers=self.admin_header)
        return response

    def test_user_can_post_menu_item_helper(self):
        '''add food item to the menu'''
        self.promote_user_helper()
        response = self.client.post(
            '/api/v2/menu',
            data=json.dumps(self.sample_menu_data),
            headers=self.admin_header)
        self.assertIn('Food item created successfully"', str(response.data))
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        drop_tables()


class TestApi(TestBase):
    """docstring for TestApi"""

    def test_to_register_a_new_user(self):
        """ The test should return status code 200 for success (POST request)"""
        response = self.registration_response
        self.assertEqual(response.status_code, 201)

    def test_user_update_their_credentials(self):
        '''method to test updating user data'''
        self.test_user_can_post_menu_item_helper()
        response = self.client.put(
            '/api/v2/auth/users/1',
            data=json.dumps(self.sample_registration_data),
            headers=self.admin_header)
        self.assertIn("User details edited successfully", str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_user_can_view_menu_items(self):
        '''method to test getting menu items'''
        self.test_user_can_post_menu_item_helper()
        response = self.client.get(
            '/api/v2/menu',
            headers=self.admin_header)
        self.assertIn("New Pizza in town", str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_user_can_order_food_item(self):
        '''Method to test user can order food'''
        response = self.client.post(
            '/api/v2/orders',
            data=json.dumps(self.sample_order_without_quantity),
            headers=self.admin_header)
        self.assertIn(
            'An integer should be input in this field', str(response.data))
        self.assertEqual(response.status_code, 400)

    def test_admin_cant_pass_an_invalid_status(self):
        '''test can't update a wrong status'''
        self.promote_user_helper()
        response = self.client.put(
            '/api/v2/orders/1',
            data=json.dumps(self.sample_invalid_status),
            headers=self.admin_header)
        self.assertIn('Invalid Status!', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_admin_cant_delete_food_item_when_not_complete(self):
        '''test that orders get deleted when status is complete'''
        self.promote_user_helper()
        response = self.client.delete(
            '/api/v2/orders/1',
            headers=self.admin_header)
        self.assertIn('No order found with that id', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_get_order_items_before_creating(self):
        '''Test that user can get order items'''
        self.promote_user_helper()
        response = self.client.get(
            '/api/v2/orders',
            headers=self.admin_header)
        self.assertIn('No orders found!', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_user_can_get_order_items_for_a_user(self):
        '''Test to get orders made by a specific user'''
        self.test_user_can_post_menu_item_helper()
        response = self.client.get(
            '/api/v2/orders/1',
            headers=self.admin_header)
        self.assertIn('message', str(response.data))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
