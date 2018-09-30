"""tests for orders.py file"""
import unittest
import json

# local imports
from app import create_app
from app.api.V1.views import FoodItems, FoodItem


class TestApi(unittest.TestCase):
    """All tests are called here"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.orders = FoodItems()
        self.others = FoodItem()
        self.app = create_app(config_name="testing").test_client()
        self.sample_order = {
            'name': 'Fish Pie',
            'price': '600'
        }

    def test_api_can_get_all_orders(self):
        """Test API can get a  list of all Orders (GET request)."""
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        test_resp = self.app.get(
            '/api/v1/orders',
            headers={'content-type': 'application/json'}
        )
        self.assertIn('Fish Pie', str(test_resp.data))
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
        self.assertIn('already exists', str(test_resp.data))

    def test_api_can_get_one_order(self):
        """Test API can get a single order (GET request)."""
        self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        test_resp = self.app.get(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )
        self.assertIn('Fish Pie', str(test_resp.data))
        self.assertEqual(
            test_resp.status_code, 200, msg='Expected 200'
        )

    def test_api_can_update_an_order(self):
        """Test API can update a specified order item (PUT request)."""

        test_resp = self.app.put(
            '/api/v1/orders/1',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        self.assertEqual(test_resp.status_code, 201)

    def test_order_item_deletion(self):
        """Test API can delete an existing orderitem. (DELETE request)."""

        res = self.app.delete(
            '/api/v1/orders/1',
            headers={'content-type': 'application/json'}
        )
        self.assertIn("Order deleted successfully", str(res.data))
        self.assertEqual(res.status_code, 200)

    def test_that_order_cant_be_duplicate(self):
        """ The test should return status code 200 for success (POST request)"""
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        test_resp = self.app.post(
            '/api/v1/orders',
            data=json.dumps(self.sample_order),
            headers={'content-type': 'application/json'}
        )
        resp = json.loads(test_resp.data.decode('utf-8'))
        self.assertEqual('Order already exists', resp['message'])


if __name__ == '__main__':
    unittest.main()
