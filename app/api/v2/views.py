"""Order api endpoits"""
import datetime
import os
from flask import jsonify, request, json
from flask_restful import Resource
import jwt
import psycopg2


conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()


class MenuItems(Resource):
    """major orders class"""

    def get(self):
        """returns all orders"""
        cur.execute('SELECT * FROM food_items;')
        orders = cur.fetchall()
        if not orders:
            return jsonify({'message': 'No food items found!'})
        order_list = []
        for order in orders:
            orders_dict = {}
            orders_dict['id'] = order[0]
            orders_dict['name'] = order[1]
            orders_dict['price'] = "$" + str(order[2])
            order_list.append(orders_dict)
        response = jsonify({'Orders': order_list})
        response.status_code = 200
        return response

    def post(self):
        """adds a new order"""
        if not active_user['admin']:
            return jsonify({'message': 'Can not perfom this action!'})
        request_data = request.get_json(force=True)
        cur.execute('SELECT * FROM food_items WHERE name = (%s);',
                    (request_data['name'],))
        order = cur.fetchone()
        if order:
            return jsonify({'message': 'Menu item already exists'})
        cur.execute("INSERT INTO food_items (name, price) VALUES (%s, %s)",
                    (request_data["name"], request_data["price"]))
        conn.commit()
        response = jsonify({'Orders': 'Food item created successfully'})
        response.status_code = 201
        return response


class OrderItems(Resource):
    """major orders class"""

    def get(self):
        """returns all orders"""
        cur.execute(
            'SELECT * FROM orders WHERE user_id = (%s);', [active_user['id']])
        orders = cur.fetchall()
        if not orders:
            return jsonify({'message': 'No orders found!'})

        order_list = []
        for order in orders:
            orders_dict = {}
            orders_dict['id'] = order[0]
            orders_dict['name'] = order[1]
            orders_dict['status'] = order[2]
            orders_dict['ordered_by'] = active_user['name']
            order_list.append(orders_dict)
        response = jsonify({'Orders': order_list})
        response.status_code = 200
        return response

    def post(self):
        """adds a new order"""
        request_data = request.get_json(force=True)
        # cur.execute('SELECT * FROM users WHERE name = (%s);',
        #             ('Admin',))
        # user = cur.fetchone()

        cur.execute('SELECT * FROM food_items WHERE name = (%s);',
                    (request_data['name'],))
        confirm_order = cur.fetchone()
        if not confirm_order:
            response = jsonify({'message': 'Food item not in our menu!'})
            response.status_code = 400
            return response

        cur.execute('SELECT * FROM orders WHERE name = (%s) AND user_id = (%s);',
                    (request_data['name'], active_user['id']))
        order = cur.fetchone()
        if order:
            response = jsonify(
                {'message': 'Similar order has already been made!'})
            response.status_code = 400
            return response
        cur.execute("INSERT INTO orders (name, user_id) VALUES (%s, %s)",
                    (request_data["name"], active_user['id']))
        conn.commit()
        response = jsonify({'Orders': 'Order created successfully'})
        response.status_code = 201
        return response


class OrderItem(Resource):
    """docstring for Others"""

    # @token
    def get(self, order_id):
        '''returns one order'''
        cur.execute('SELECT * FROM orders WHERE id = (%s);', (order_id,))
        order = cur.fetchone()
        if not order:
            return jsonify({"message": "No order was found with that id"})
        order_details = {}
        order_details['id'] = order[0]
        order_details['name'] = order[1]
        order_details['status'] = order[2]
        response = jsonify({'order': order_details})
        response.status_code = 200
        return response

    # @token
    def put(self, order_id):
        """updates an order"""
        request_data = request.get_json(force=True)
        cur.execute('SELECT * FROM orders WHERE id = (%s);', (order_id,))
        order = cur.fetchone()
        if not order:
            return jsonify({'message': 'No order found with that id'})
        cur.execute('UPDATE orders SET status = (%s) WHERE id = (%s);',
                    (request_data['status'], order_id))
        conn.commit()
        response = jsonify({'Order': 'Order Status updated successfully'})
        response.status_code = 201
        return response

    # @token
    def delete(self, order_id):
        """deletes an oder"""
        cur.execute('SELECT * FROM orders WHERE id = (%s);', (order_id,))
        order = cur.fetchone()
        if not order:
            return jsonify({'message': 'No order found with that id'})
        cur.execute('DELETE FROM orders WHERE id = (%s);', (order_id,))
        conn.commit()
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
