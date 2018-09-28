"""Order api endpoits"""
from flask import jsonify, request
from flask_restful import Resource


ORDERS = []
USERS = []


class FoodItems(Resource):
    """major orders class"""

    def get(self):
        """returns all orders"""
        if len(ORDERS) == 0:
            return jsonify({'message': 'No orders found!'})
        response = jsonify({'Orders': ORDERS})
        response.status_code = 200
        return response

    def post(self):
        """adds a new order"""
        request_data = request.get_json(force=True)
        order = [order for order in ORDERS if order[
            'name'] == request_data["name"]]
        if request_data["name"] == "" or request_data["price"] == "":
            return jsonify({'message': 'Name field must be filled.'})
        if order:
            return jsonify({'message': 'Order already exists'})
        new_order = {
            'id': len(ORDERS) + 1,
            'name': request_data["name"],
            'price': request_data["price"]
        }
        ORDERS.append(new_order)
        response = jsonify({'message': 'order item created successfully!'})
        response.status_code = 201
        return response


class FoodItem(Resource):
    """docstring for Others"""

    def get(self, order_id):
        """returns one order from the list"""
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})
        response = jsonify({'Order': order})
        response.status_code = 200
        return response

    # @token
    def put(self, order_id):
        """updates an order"""
        request_data = request.get_json(force=True)
        order = [order for order in ORDERS if order['id'] == order_id]
        if request_data["name"] == "" or request_data["price"] == "":
            return jsonify({'message': 'Name field must be filled.'})
        if not order:
            return jsonify({'message': 'No order found with that id'})

        order[0]['name'] = request_data['name']
        order[0]['price'] = request_data['price']
        response = jsonify({'message': 'order updated succesfully'})
        response.status_code = 201
        return response

    def delete(self, order_id):
        """deletes an oder"""
        order = [order for order in ORDERS if order['id'] == order_id]
        if not order:
            return jsonify({'message': 'No order found with that id'})
        ORDERS.remove(order[0])
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
