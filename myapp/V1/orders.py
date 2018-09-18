"""Order api endpoits"""
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
APP = Flask(__name__)
API = Api(APP)

ORDERS = []


class Orders(Resource):
    """major orders class"""

    def get(self):
        """returns all orders"""
        if len(ORDERS) == 0:
            return jsonify({'message': 'No orders found!'})
        # return jsonify({'Orders': ORDERS}), 200
        response = jsonify({'Orders': ORDERS})
        response.status_code = 200
        return response

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


class Others(Resource):
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

    def put(self, order_id):
        """updates an order"""
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})

        request_data = request.get_json(force=True)
        edit_order = [order for order in ORDERS if order['id'] == order_id]
        edit_order[0]['name'] = request_data['name']
        edit_order[0]['price'] = request_data['price']
        response = jsonify({'Order': edit_order})
        response.status_code = 201
        return response

    def delete(self, order_id):
        """deletes an oder"""
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})
        ORDERS.remove(order[0])
        # return jsonify({'message': 'Order deleted successfully'}), 200
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response


API.add_resource(Orders, '/api/v1/orders')
API.add_resource(Others, '/api/v1/orders/<int:order_id>')
