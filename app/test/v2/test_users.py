"""tests for orders.py file"""
import unittest
import json

# local imports
from app import create_app


class TestApi(unittest.TestCase):
    """All tests are called here"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app("testing").test_client()
        self.sample_user = {
            "name": "Admin",
            "password": "password"
        }

    def test_to_register_a_new_user(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.app.post(
            '/api/v2/users',
            data=json.dumps(self.sample_user),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 200)

    def test_to_login_a_user(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.app.post(
            '/api/v2/users',
            data=json.dumps(self.sample_user),
            headers={'content-type': 'application/json'}
        )
        self.assertIn('User already exists', str(test_resp.data))
        self.assertEqual(test_resp.status_code, 200)

    def test_api_cannot_get_all_users(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.app.get(
            '/api/v2/users',
            headers={'content-type': 'application/json'}
        )
        self.assertIn('Ensure you are logged in to get a token!',
                      str(test_resp.data))
        self.assertEqual(
            test_resp.status_code, 401
        )

    def test_api_can_get_all_menu_items(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.app.get(
            '/api/v2/menu',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200
        )

    def test_api_can_get_all_orders(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.app.get(
            '/api/v2/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 401
        )

    def test_that_user_should_be_authenticated(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.app.post(
            '/api/v2/orders',
            data=json.dumps(self.sample_user),
            headers={'content-type': 'application/json'}
        )

        # self.assertIn('Fish Pie', test_resp)
        resp = json.loads(test_resp.data.decode('utf-8'))
        self.assertEqual(
            'Ensure you are logged in to get a token!', resp['message'])


if __name__ == '__main__':
    unittest.main()