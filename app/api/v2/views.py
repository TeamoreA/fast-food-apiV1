"""Order api endpoits"""
import datetime
import os
from flask import jsonify, request, json
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from .models import token
from .datamodels import get_all_users, single_user_email, single_user_name,\
    post_users, single_user_id, promote_user, update_user,\
    delete_user, post_menu_items, single_menu_name, get_all_menuitems,\
    get_all_orders, post_order_item, check_user_orders, delete_order,\
    single_order_id, update_order, single_order_user_id


class Users(Resource):

    @token
    def get(self, active_user):
        '''return all users'''
        users = get_all_users()
        if not users:
            return jsonify({"message": "No user has been created yet"})
        users_list = []
        for user in users:
            user_details = {}
            user_details['id'] = user[0]
            user_details['name'] = user[1]
            user_details['email'] = user[2]
            user_details['password'] = user[3]
            user_details['admin'] = user[4]
            users_list.append(user_details)
        response = jsonify({"Users": users_list})
        response.status_code = 200
        return response

    def post(self):
        """method to get all users"""
        request_data = request.get_json(force=True)
        if not request_data and request_data['name'] == ''and request_data['email'] == '':
            return jsonify({'message': 'No empty fields allowed!'})
        user = single_user_email(request_data['email'])
        if user:
            return jsonify({'message': 'User already exists'})
        chars = ['.', '@']
        email = request_data['email']
        for i in range(len(email)):
            if email[i].isalpha and email[i] in chars:
                checked_mail = email
        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        post_users(request_data["name"], checked_mail, hashed_pw)
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
        request_data = request.get_json(force=True)
        user = single_user_id(user_id)
        if not user:
            return jsonify({'message': 'No user found with that id'})

        hashed_pw = generate_password_hash(
            request_data['password'], method='sha256')
        update_user(request_data['name'], request_data[
            'email'], hashed_pw, user_id)
        response = jsonify({"message": "User details edited successfully"})
        response.status_code = 201
        return response

    @token
    def get(self, active_user, user_id):
        '''returns one user'''
        user = single_user_id(user_id)
        if not user:
            return jsonify({"message": "No user was found with that id"})
        user_details = {}
        user_details['id'] = user[0]
        user_details['name'] = user[1]
        user_details['email'] = user[2]
        user_details['password'] = user[3]
        user_details['admin'] = user[4]
        response = jsonify({'User': user_details})
        response.status_code = 200
        return response

    @token
    def delete(self, active_user, user_id):
        """deletes a user"""
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
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            response = jsonify({'message': 'Login is required!'})
            response.status_code = 401
            return response
        user = single_user_name(auth.username)
        if not user:
            response = jsonify({'message': 'User not found!'})
            response.status_code = 401
            return response
        if check_password_hash(user[3], auth.password):
            token = jwt.encode({'id': user[0], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=45)}, os.getenv('SECRET'))
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
        response = jsonify({'Menu List': menu_list})
        response.status_code = 200
        return response

    @token
    def post(self, active_user):
        """adds a new order"""
        if not active_user['admin']:
            return jsonify({'message': 'Can not perfom this action!'})
        request_data = request.get_json(force=True)
        food_item = single_menu_name(request_data["name"])
        if food_item:
            return jsonify({'message': 'Menu item already exists'})
        post_menu_items(request_data["name"], request_data[
            "price"], request_data["description"])
        response = jsonify({'Orders': 'Food item created successfully'})
        response.status_code = 201
        return response


class OrderItems(Resource):
    """major orders class"""
    @token
    def get(self, active_user):
        """returns all orders"""
        if not active_user['admin']:
            return jsonify({"message": "Cannot perform this action"})
        orders = get_all_orders()
        if not orders:
            return jsonify({'message': 'No orders found!'})
        order_list = []
        for order in orders:
            user = single_user_id([order[3]])
            orders_dict = {}
            orders_dict['id'] = order[0]
            orders_dict['name'] = order[1]
            orders_dict['status'] = order[2]
            orders_dict['ordered_by'] = user[1]
            order_list.append(orders_dict)
        response = jsonify({'Orders': order_list})
        response.status_code = 200
        return response

    @token
    def post(self, active_user):
        """adds a new order"""
        request_data = request.get_json(force=True)
        if request_data["name"] == "" or request_data["price"] == "":
            return jsonify({'message': 'Name field must be filled.'})
        confirm_order = single_menu_name(request_data['name'])
        if not confirm_order:
            response = jsonify({'message': 'Food item not in our menu!'})
            response.status_code = 400
            return response
        order = single_order_user_id(request_data['name'], active_user['id'])
        if order:
            response = jsonify(
                {'message': 'Similar order has already been made!'})
            response.status_code = 400
            return response
        post_order_item(request_data["name"], active_user['id'])
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
            user = single_user_id(order[3])
            order_details = {}
            order_details['id'] = order[0]
            order_details['name'] = order[1]
            order_details['status'] = order[2]
            order_details['ordered_by'] = user[1]
            order_list.append(order_details)
        response = jsonify({'orders': order_list})
        response.status_code = 200
        return response

    @token
    def put(self, active_user, order_id):
        """updates an order"""
        if not active_user['admin']:
            return jsonify({"message": "Cannot perform this action"})
        request_data = request.get_json(force=True)
        if request_data["name"] == "" or request_data["price"] == "":
            return jsonify({'message': 'Name field must be filled.'})
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
        user = single_user_id(order[3])
        if not user:
            return jsonify({'message': 'Permission denied! This is not your order item'})
        delete_order(order_id)
        response = jsonify({'message': 'Order deleted successfully'})
        response.status_code = 200
        return response
