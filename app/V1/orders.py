"""Order api endpoits"""
from flask import Flask, jsonify, request
APP = Flask(__name__)

ORDERS = []

# Route containing function to return all orders


@APP.route('/api/v1/orders', methods=['GET'])
def return_all_orders():
    """returns all orders"""
    if len(ORDERS) == 0:
        return jsonify({'message': 'No orders found!'})
    return jsonify({'Orders': ORDERS})

# Route containing function to return one order using its name


@APP.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def return_one_order(order_id):
    """returns one order from the list"""
    order = [order for order in ORDERS if order['id'] == order_id]
    # if order == "":
    #     abort(404)
    if not order:
        return jsonify({'message': 'No order found with that id'})
    return jsonify({'Order': order})

# Route containing function to add new order name


@APP.route('/api/v1/orders', methods=['POST'])
def add_order():
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
    return jsonify({'Orders': ORDERS}), 201

# Route with a function to update a single order


@APP.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def edit_an_order(order_id):
    """updates an order"""
    order = [order for order in ORDERS if order['id'] == order_id]
    if not order:
        return jsonify({'message': 'No order found with that id'})

    request_data = request.get_json()
    edit_order = [order for order in ORDERS if order['id'] == order_id]
    edit_order['name'] = request_data['name']
    edit_order['price'] = request_data['price']
    return jsonify({'Order': edit_order})

# this endpoint deletes the specified(using its id) order from dictionary


@APP.route('/api/v1/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """deletes an oder"""
    order = [order for order in ORDERS if order['id'] == order_id]
    if not order:
        return jsonify({'message': 'No order found with that id'})
    ORDERS.remove(order[0])
    return jsonify({'message': 'Order deleted successfully'}), 200

if __name__ == '__main__':
    APP.run(debug=True)
