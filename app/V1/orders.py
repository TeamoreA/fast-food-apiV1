from flask import Flask, jsonify, request
APP = Flask(__name__)

ORDERS = [
    {
        'id': 1,
        "name": "Pizza",
        "price": "$99"
    },
    {
        'id': 2,
        "name": "Chicken",
        "price": "$550"
    },
    {
        'id': 3,
        "name": "Burger",
        "price": "$490"
    },
    {
        'id': 4,
        "name": "French Fries",
        "price": "$399"
    }
]

# Route containing function to return all orders


@APP.route('/api/v1/orders', methods=['GET'])
def return_all_orders():
    """returns all orders"""
    return jsonify({'Orders': ORDERS})

# Route containing function to return one order using its name


@APP.route('/api/v1/orders/<int:order_id>', methods=['GET'])
def return_one_order(order_id):
    """returns one order from the list"""
    order = [order for order in ORDERS if order['id'] == order_id]
    # if order == "":
    #     abort(404)
    return jsonify({'Order': order})

# Route containing function to add new order name


@APP.route('/api/v1/orders', methods=['POST'])
def add_order():
    """adds a new order"""
    request_data = request.get_json()
    new_order = {
        'id': ORDERS[-1]['id'] + 1,
        'name': request_data["name"],
        'price': request_data["price"]
    }
    ORDERS.append(new_order)
    return jsonify({'Order': new_order}), 201

# Route with a function to update a single order


@APP.route('/api/v1/orders/<int:order_id>', methods=['PUT'])
def edit_an_order(order_id):
    request_data = request.get_json()
    edit_order = [order for order in ORDERS if order['id'] == order_id]
    edit_order[0]['name'] = request_data['name']
    edit_order[0]['price'] = request_data['price']
    return jsonify({'Order': edit_order[0]})

if __name__ == '__main__':
    APP.run(debug=True)
