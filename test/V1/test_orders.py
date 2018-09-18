"""tests for orders.py file"""
import unittest
import json
from myapp.V1.orders import Orders, Others, APP


class TestApi(unittest.TestCase):
    """All tests are called here"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.orders = Orders()
        self.others = Others()
        self.app = APP.test_client()
        self.sample_order = {
            'name': 'Fish Pie',
            'price': '$460'
        }
        self.get_order = {
            "name": "Pizza",
            'price': '$460'
        }

    def test_api_can_get_all_orders(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.app.get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        # resp = self.orders.post('/api/v1/orders', new_order=self.sample_order)
        # self.assertEqual(resp.status_code, 201)
        # resp = self.app.get('/api/v1/orders')
        # self.assertEqual(resp.status_code, 200)
        # self.assertIn('Fish Pie', str(resp.data))
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_api_can_get_one_order(self):
        """Test API can get a single order (GET request)."""
        test_resp = self.app.get(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_create_new_order(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        # self.assertIn('Fish Pie', test_resp)
        self.assertEqual(test_resp.status_code, 201)

    def test_api_can_update_an_order(self):
        """Test API can update a specified order item (PUT request)."""

        test_resp = self.app.put(
            '/api/v1/orders/1',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 200)

    def test_order_item_deletion(self):
        """Test API can delete an existing orderitem. (DELETE request)."""
        res = self.app.delete(
            '/api/v1/orders/2',
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
