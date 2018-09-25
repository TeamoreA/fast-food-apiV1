"""Order api endpoits"""
# import os
from flask import jsonify, request
from flask_restful import Resource

# APP = Flask(__name__)
# API = Api(APP)

# APP.config['SECRET_KEY'] = os.environ.get('APP_SETTINGS')

ORDERS = []
USERS = []


class OrdersV1(Resource):
    """major orders class"""

    # @token
    def get(self):
        """returns all orders"""
        if len(ORDERS) == 0:
            return jsonify({'message': 'No orders found!'})
        # return jsonify({'Orders': ORDERS}), 200
        response = jsonify({'Orders': ORDERS})
        response.status_code = 200
        return response

    # @token
    def post(self):
        """adds a new order"""
        request_data = request.get_json(force=True)
        order = [order for order in ORDERS if order[
            'name'] == request_data["name"]]
        if order:
            return jsonify({'message': 'Order already exists'})
        new_order = {
            'id': len(ORDERS) + 1,
            'name': request_data["name"],
            'price': request_data["price"]
        }
        ORDERS.append(new_order)
        response = jsonify({'Orders': ORDERS})
        response.status_code = 201
        return response


class OtherOrdersV1(Resource):
    """docstring for Others"""

    def get(self, order_id):
        """returns one order from the list"""
        order = [order for order in ORDERS if order['id'] == order_id]
        # if order == "":
        #     abort(404)
        if not order:
            return jsonify({'message': 'No order found with that id'})
        # return jsonify({'Order': order}), 200
        response = jsonify({'Order': order})
        response.status_code = 200
        return response

    # @token
    def put(self, order_id):
        """updates an order"""
        request_data = request.get_json(force=True)
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})

        # edit_order = [order for order in ORDERS if order['id'] == order_id]
        order[0]['name'] = request_data['name']
        order[0]['price'] = request_data['price']
        response = jsonify({'Order': order})
        response.status_code = 201
        return response

    # @token
    def delete(self, order_id):
        """deletes an oder"""
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})
        ORDERS.remove(order[0])
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
