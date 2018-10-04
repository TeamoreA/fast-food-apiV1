"""Order api endpoits"""
import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
import jwt
import psycopg2
from instance.config import Config
from .models import token, Validators
from .datamodels import single_user_name,\
    post_users, single_user_id, promote_user, update_user,\
    delete_user, post_menu_items, single_menu_name, get_all_menuitems,\
    get_all_orders, post_order_item, check_user_orders, delete_order,\
    single_order_id, update_order


conn = psycopg2.connect(Config.DATABASE_URL)


class Users(Resource):
    """users major class"""

    def post(self):
        """method to get all users"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('email', type=str, required=True,
                            help="Email field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        parser.add_argument('confirm_password', type=str, required=True,
                            help="Confirm_password field is required")
        request_data = parser.parse_args()
        if request_data['password'] != request_data['confirm_password']:
            return jsonify({'message': 'your passwords are inconsistent!'})
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid user name!'})
        if not Validators().valid_email(request_data['email']):
            return jsonify({'message': 'Invalid user email!'})
        user = single_user_name(request_data['name'])
        if user:
            return jsonify({'message': 'User already exists'})
        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        post_users(request_data["name"], request_data['email'], hashed_pw)
        response = jsonify(
            {'Message': 'New user has been created successfully'})
        response.status_code = 201
        return response


class PromoteUser(Resource):
    """docstring for OtherUsers"""
    @token
    def put(self, active_user, user_id):
        """Updates users password"""
        user = single_user_id(1)
        if not user:
            return jsonify({'message': 'Sorry you can not perform this function'})
        promote_user(user_id)
        response = jsonify({"message": "User is an admin now"})
        response.status_code = 201
        return response


class User(Resource):
    """docstring for OtherUsers"""
    @token
    def put(self, active_user, user_id):
        """Updates users password"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('email', type=str, required=True,
                            help="Email field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        request_data = parser.parse_args()
        user = single_user_id(user_id)
        if not user:
            return jsonify({'message': 'No user found with that id'})
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid user name!'})
        if not Validators().valid_email(request_data['email']):
            return jsonify({'message': 'Invalid user email!'})
        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        update_user(request_data['name'], request_data[
            'email'], hashed_pw, user_id)
        response = jsonify({"message": "User details edited successfully"})
        response.status_code = 201
        return response

    @token
    def delete(self, active_user, user_id):
        """deletes a user"""
        if not active_user['admin']:
            return jsonify({'message': 'Can not perfom this action, Admin privilege required!'})
        user = single_user_name(user_id)
        if not user:
            return jsonify({'message': 'No user found with that name, The name is case sensitive'})
        delete_user(user_id)
        response = jsonify({'message': 'User deleted successfully'})
        response.status_code = 200
        return response


class Login(Resource):
    """docstring for Login"""

    def post(self):
        """login route"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['name']):
            return {'message': 'Please enter a valid name'}, 400
        user = single_user_name(request_data['name'])
        if not user:
            response = jsonify({'message': 'User not found!'})
            response.status_code = 401
            return response
        if check_password_hash(user[3], request_data['password']):
            token = jwt.encode({'id': user[0], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=60)}, Config.SECRET_KEY)
            return jsonify({'token': token.decode('UTF-8')})
        response = jsonify({'message': 'Login required!'})
        response.status_code = 401
        return response


class MenuItems(Resource):
    """major orders class"""

    def get(self):
        """returns all orders"""
        menu_items = get_all_menuitems()
        if not menu_items:
            return jsonify({'message': 'No food items found!'})
        menu_list = []
        for menu_item in menu_items:
            orders_dict = {}
            orders_dict['id'] = menu_item[0]
            orders_dict['name'] = menu_item[1]
            orders_dict['price'] = "$" + str(menu_item[2])
            orders_dict['description'] = menu_item[3]
            menu_list.append(orders_dict)
        response = jsonify(
            {'message': 'Available food items in the menu', 'Menu List': menu_list})
        response.status_code = 200
        return response

    @token
    def post(self, active_user):
        """adds a new order"""
        if not active_user['admin']:
            return jsonify({'message': 'Can not perfom this action, Admin privilege required!'})
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('price', type=float, required=True,
                            help="Price field is required")
        parser.add_argument('description', type=str, required=True,
                            help="Description field is required")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})
        if not Validators().validate_name(request_data['description']):
            return jsonify({'message': 'Invalid Description!'})
        food_item = single_menu_name(request_data["name"])
        if food_item:
            return jsonify({'message': 'Menu item already exists'})
        post_menu_items(request_data["name"], request_data[
            "price"], request_data["description"])
        response = jsonify({'Menu': 'Food item created successfully'})
        response.status_code = 201
        return response


class OrderItems(Resource):
    """major orders class"""
    @token
    def get(self, active_user):
        """returns all orders"""
        if not active_user['admin']:
            return jsonify({"message": "Cannot perform this action, Admin privilege required!"})
        orders = get_all_orders()
        if not orders:
            return jsonify({'message': 'No orders found!'})
        order_list = []
        for order in orders:
            user = single_user_id(order[5])
            orders_dict = {}
            orders_dict['id'] = order[0]
            orders_dict['name'] = order[1]
            orders_dict['address'] = order[2]
            orders_dict['quantity'] = order[3]
            orders_dict['status'] = order[4]
            orders_dict['ordered_by'] = user[1]
            order_list.append(orders_dict)
        response = jsonify({'Orders': order_list})
        response.status_code = 200
        return response

    @token
    def post(self, active_user):
        """adds a new order"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('address', type=str, required=True,
                            help="Address field is required")
        parser.add_argument('quantity', type=int, required=True,
                            help="An integer should be input in this field")
        request_data = parser.parse_args()
        confirm_order = single_menu_name(request_data['name'])
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})

        if not Validators().validate_name(request_data['address']):
            return jsonify({'message': 'Invalid address!'})
        if not confirm_order:
            response = jsonify({'message': 'Food item not in our menu!'})
            response.status_code = 400
            return response
        post_order_item(request_data["name"], request_data[
            'address'], request_data['quantity'], active_user['id'])
        response = jsonify({'Orders': 'Order created successfully'})
        response.status_code = 201
        return response


class OrderItem(Resource):
    """docstring for Others"""

    @token
    def get(self, active_user, order_id):
        '''returns one order'''
        orders = check_user_orders(order_id)
        if not orders:
            return jsonify({"message": "No orders found for that user"})
        order_list = []
        for order in orders:
            user = single_user_id(order[5])
            order_details = {}
            order_details['id'] = order[0]
            order_details['name'] = order[1]
            order_details['address'] = order[2]
            order_details['quantity'] = order[3]
            order_details['status'] = order[4]
            order_details['ordered_by'] = user[1]
            order_list.append(order_details)
        response = jsonify({'orders': order_list})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, order_id):
        """updates an order"""
        if not active_user['admin']:
            return jsonify({"message": "Cannot perform this action, Admin privilege required!"})
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True,
                            help="Status field is required")
        request_data = parser.parse_args()
        if not Validators().validate_status(request_data['status']):
            return jsonify({'message': 'Invalid Status!'})
        order = single_order_id(order_id)
        if not order:
            return jsonify({'message': 'No order found with that id'})
        update_order(request_data['status'], order_id)
        response = jsonify({'Order': 'Order Status updated successfully'})
        response.status_code = 201
        return response

    @token
    def delete(self, active_user, order_id):
        """deletes an oder"""
        order = single_order_id(order_id)
        if not order:
            return jsonify({'message': 'No order found with that id'})
        user = single_user_id(order[5])
        if not user:
            return jsonify({'message': 'Permission denied! This is not your order item'})
        if order[4] != 'Complete':
            response = jsonify({'message': 'Order should be completed first!'})
        delete_order(order_id)
        conn.close()
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
