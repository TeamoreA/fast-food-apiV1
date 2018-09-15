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
    '''returns all orders'''
    return jsonify({'Orders': ORDERS})


if __name__ == '__main__':
    APP.run(debug=True)
