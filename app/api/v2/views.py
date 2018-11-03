"""Order api endpoits"""
import datetime
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, reqparse
import jwt
import psycopg2
from instance.config import Config
from .models import token, Validators
from .datamodels import single_user_email, single_user_name,\
    post_users, single_user_id, promote_user, update_user,\
    delete_user, post_menu_items, single_menu_name, get_all_menuitems,\
    get_all_orders, post_order_item, check_user_orders, delete_order,\
    single_order_id, update_order_status, get_all_users, single_menu_id,\
    delete_menu, update_menu, update_order


conn = psycopg2.connect(Config.DATABASE_URL)


class Users(Resource):
    """users major class"""

    def post(self):
        """method to get all users"""
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help="username field is required")
        parser.add_argument('email', type=str, required=True,
                            help="Email field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        parser.add_argument('confirm_password', type=str, required=True,
                            help="Confirm_password field is required")
        request_data = parser.parse_args()
        if request_data['password'] != request_data['confirm_password']:
            return jsonify({'message': 'your passwords are inconsistent!'})
        if not Validators().validate_name(request_data['username']):
            return jsonify({'message': 'Invalid user name!'})
        if not Validators().valid_email(request_data['email']):
            return jsonify({'message': 'Invalid user email!'})
        if not Validators().validate_password(request_data['password']):
            return jsonify({'message': 'password must be between 6 and 60 letters!'})
        user = single_user_name(request_data['username'])
        if user:
            response_data = jsonify({'message': 'username already taken'})
            response_data.status_code = 409
            return response_data
        email = single_user_email(request_data['email'])
        if email:
            response_data = jsonify({'message': 'Email already taken'})
            response_data.status_code = 409
            return response_data
        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        post_users(request_data["username"], request_data['email'], hashed_pw)
        response = jsonify(
            {'message': 'New user has been created successfully'})
        response.status_code = 201
        return response

    def get(self):
        """returns all users"""
        users = get_all_users()
        if not users:
            return jsonify({'message': 'No users found!'})
        users_list = []
        for user in users:
            users_dict = {}
            users_dict['id'] = user[0]
            users_dict['name'] = user[1]
            users_dict['email'] = user[2]
            users_dict['admin'] = user[4]
            users_list.append(users_dict)
        response = jsonify({'Users': users_list})
        response.status_code = 200
        return response


class PromoteUser(Resource):
    """docstring for OtherUsers"""

    @token
    def put(self, active_user, user_id):
        """Updates users password"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
        promote_user(user_id)
        response = jsonify({"message": "User is an admin now"})
        response.status_code = 200
        return response


class SingleUser(Resource):
    """docstring for OtherUsers"""

    def get(self, user_id):
        '''returns one user'''
        user = single_user_id(user_id)
        if not user:
            response_data = jsonify({'message': 'No user found with that id'})
            response_data.status_code = 404
            return response_data

        user_details = {}
        user_details['id'] = user[0]
        user_details['name'] = user[1]
        user_details['email'] = user[2]
        user_details['admin'] = user[4]
        response = jsonify(
            {'user': user_details})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, user_id):
        """Updates users password"""
        if active_user['id'] != user_id:
            response_data = jsonify(
                {"message": "Not allowed!"})
            response_data.status_code = 403
            return response_data
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help="username field is required")
        parser.add_argument('email', type=str, required=True,
                            help="Email field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        request_data = parser.parse_args()
        user = single_user_id(user_id)
        if not user:
            return jsonify({'message': 'No user found with that id'})
        if not Validators().validate_name(request_data['username']):
            return jsonify({'message': 'Invalid user username!'})
        if not Validators().valid_email(request_data['email']):
            return jsonify({'message': 'Invalid user email!'})
        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        update_user(request_data['username'], request_data[
            'email'], hashed_pw, user_id)
        response = jsonify({"message": "User details edited successfully"})
        response.status_code = 200
        return response

    @token
    def delete(self, active_user, user_id):
        """deletes a user"""
        if active_user['id'] != user_id:
            response_data = jsonify(
                {"message": "Not allowed!"})
            response_data.status_code = 403
            return response_data
        user = single_user_id(user_id)
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
        parser.add_argument('username', type=str, required=True,
                            help="username field is required")
        parser.add_argument('password', type=str, required=True,
                            help="Password field is required")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['username']):
            return {'message': 'Please enter a valid name'}, 400
        user = single_user_name(request_data['username'])
        if not user:
            response = jsonify({'message': 'User not found!'})
            response.status_code = 401
            return response
        if check_password_hash(user[3], request_data['password']):
            token = jwt.encode({'id': user[0], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=60)}, Config.SECRET_KEY)
            return jsonify({'message': 'Welcome ' + request_data['username'] + ', You logged in successfully',
                            'token': token.decode('UTF-8')})
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
            orders_dict['image'] = menu_item[4]
            menu_list.append(orders_dict)
        response = jsonify(
            {'message': 'Available food items in the menu', 'menu': menu_list})
        response.status_code = 200
        return response

    @token
    def post(self, active_user):
        """adds a new order"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('price', type=float, required=True,
                            help="Price field is required")
        parser.add_argument('description', type=str, required=True,
                            help="Description field is required")
        parser.add_argument('image', type=str, required=True,
                            help="Image URL field is required")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})
        if not Validators().validate_price(request_data['price']):
            return jsonify({'message': 'Price must be a positive number greater than zero.'})
        food_item = single_menu_name(request_data["name"])
        if food_item:
            return jsonify({'message': 'Menu item already exists'})
        post_menu_items(request_data["name"], request_data["price"], request_data[
                        "description"], request_data["image"])
        response = jsonify({'message': 'Food item created successfully'})
        response.status_code = 201
        return response


class SingleMenu(Resource):
    """Class for accessing individual food menus"""
    @token
    def delete(self, active_user, menu_id):
        """deletes an oder"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
        menu_item = single_menu_id(menu_id)
        if not menu_item:
            response_data = jsonify(
                {'message': 'No menu item found with that id'})
            response_data.status_code = 404
            return response_data
        delete_menu(menu_id)
        conn.close()
        response = jsonify({'message': 'Menu item deleted successfully'})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, menu_id):
        """updates an order"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('price', type=float, required=True,
                            help="Price field is required")
        parser.add_argument('description', type=str, required=True,
                            help="Description field is required")
        parser.add_argument('image', type=str, required=True,
                            help="Image URL field is required")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})
        if not Validators().validate_price(request_data['price']):
            return jsonify({'message': 'Price must be a positive number greater than zero.'})
        menu_item = single_menu_id(menu_id)
        if not menu_item:
            response_data = jsonify(
                {'message': 'No menu item found with that id'})
            response_data.status_code = 404
            return response_data
        update_menu(request_data["name"], request_data["price"], request_data[
            "description"], request_data["image"], menu_id)
        response = jsonify({'message': 'Food item updated successfully'})
        response.status_code = 200
        return response


class OrderItems(Resource):
    """major orders class"""
    @token
    def get(self, active_user):
        """returns all orders"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
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
        if not confirm_order:
            response = jsonify({'message': 'Food item not in our menu!'})
            response.status_code = 400
            return response
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})
        if not Validators().validate_name(request_data['address']):
            return jsonify({'message': 'Invalid address!'})
        post_order_item(request_data["name"], request_data[
            'address'], request_data['quantity'], active_user['id'])
        response = jsonify({'message': 'Order created successfully'})
        response.status_code = 201
        return response


class UserOrders(Resource):
    """docstring for Others"""

    @token
    def get(self, active_user, user_id):
        '''returns one order'''
        orders = check_user_orders(user_id)
        if not orders:
            response_data = jsonify(
                {"message": "No orders found for that user"})
            response_data.status_code = 404
            return response_data
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
        response = jsonify({'message': 'Users orders', 'orders': order_list})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, user_id):
        """updates an order"""
        orders = single_order_id(user_id)
        if not orders:
            response_data = jsonify(
                {"message": "No order found with that id"})
            response_data.status_code = 404
            return response_data
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help="name field is required")
        parser.add_argument('address', type=str, required=True,
                            help="Address field is required")
        parser.add_argument('quantity', type=int, required=True,
                            help="An integer should be input in this field")
        request_data = parser.parse_args()
        if not Validators().validate_name(request_data['name']):
            return jsonify({'message': 'Invalid name!'})
        if not Validators().validate_price(request_data['quantity']):
            return jsonify({'message': 'Quantity must be a positive number greater than zero.'})
        order = single_order_id(user_id)
        if not order:
            response_data = jsonify(
                {'message': 'No order found with that id'})
            response_data.status_code = 404
            return response_data
        if (order[4] == "Processing"):
            resp = jsonify(
                {'message': 'Can\'t perform this action!Order is being processed'})
            resp.status_code = 403
            return resp
        update_order(request_data["name"], request_data["address"], request_data[
            "quantity"], user_id)
        response = jsonify({'message': 'Order item updated successfully'})
        response.status_code = 200
        return response


class OrderItem(Resource):
    """docstring for Others"""

    @token
    def get(self, active_user, order_id):
        '''returns one order'''
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 404
            return response_data
        order = single_order_id(order_id)
        if not order:
            response_data = jsonify({'message': 'No order found with that id'})
            response_data.status_code = 404
            return response_data

        user = single_user_id(order[5])
        order_details = {}
        order_details['id'] = order[0]
        order_details['name'] = order[1]
        order_details['address'] = order[2]
        order_details['quantity'] = order[3]
        order_details['status'] = order[4]
        order_details['ordered_by'] = user[1]
        response = jsonify(
            {'message': 'order', 'orders': order_details})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, order_id):
        """updates an order"""
        if not active_user['admin']:
            response_data = jsonify(
                {"message": "Cannot perform this action, Admin privilege required!"})
            response_data.status_code = 403
            return response_data
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True,
                            help="Status field is required")
        request_data = parser.parse_args()
        if not Validators().validate_status(request_data['status']):
            return jsonify({'message': 'Invalid Status!'})
        order = single_order_id(order_id)
        if not order:
            response_data = jsonify({'message': 'No order found with that id'})
            response_data.status_code = 404
            return response_data

        update_order_status(request_data['status'], order_id)
        response = jsonify({'message': 'Order Status updated successfully'})
        response.status_code = 200
        return response

    @token
    def delete(self, active_user, order_id):
        """deletes an oder"""
        order = single_order_id(order_id)
        if not order:
            response_data = jsonify({'message': 'No order found with that id'})
            response_data.status_code = 404
            return response_data
        user = single_user_id(order[5])
        if not user:
            return jsonify({'message': 'Permission denied! This is not your order item'})
        if (order[4] == "Processing"):
            resp = jsonify(
                {'message': 'Can\'t perform this action!Order is being processed'})
            resp.status_code = 403
            return resp
        delete_order(order_id)
        conn.close()
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
