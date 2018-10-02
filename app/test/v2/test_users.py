"""tests for orders.py file"""
import unittest
import json

# local imports
from app import create_app


class TestBase(unittest.TestCase):
    """Base class for all tests"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing").test_client()
        self.headers = {'content-type': 'application/json'}
        self.sample_registration_data = {
            "name": "Admin",
            "email": "admin@app.com",
            "password": "password"
        }
        self.sample_login_data = {
            "name": "Admin",
            "password": "password"
        }

        # register admin user
        self.registration_helper(self.sample_registration_data)

        self.login_response = self.login_helper(self.sample_login_data)

    def registration_helper(self, registration_data):
        '''Helper method to register a user'''

        response = self.app.post(
            '/api/v2/users',
            data=json.dumps(registration_data),
            headers=self.headers)
        return response

    def login_helper(self, login_data):
        '''login helper funnction'''
        test_response = self.app.post(
            '/api/v2/login',
            data=json.dumps(login_data),
            headers=self.headers)
        response_data = json.loads(test_response.data.decode('utf-8'))['token']
        print(response_data)


class TestApi(TestBase):
    """docstring for TestApi"""

    def test_to_register_a_new_user(self):
        """ The test should return status code 200 for success (POST request)"""
        response = self.app.post(
            '/api/v2/users',
            data=json.dumps(self.sample_registration_data),
            headers=self.headers)
        print(response)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
