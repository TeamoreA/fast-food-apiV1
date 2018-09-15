import unittest
import json
from app.V1.orders import APP


class MyApiTests(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.APP = APP.test_client()
        self.sample_order = {
            'id': '4',
            'name': 'Fish Pie',
            'price': '$460'
        }
        self.get_order = {
            'id': 1,
            "name": "Pizza",
            'price': '$460'
        }

    def test_api_can_get_all_orders(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.APP.get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_api_can_get_one_order(self):
        """Test API can get a single order (GET request)."""
        test_resp = self.APP.get(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_create_new_order(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.APP.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
