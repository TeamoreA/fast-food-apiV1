""" initialise the app"""
from os import getenv
from flask import Flask
from flask_restful import Resource, Api
from instance.config import app_config
from app.api.V1.views import FoodItem, FoodItems
from app.api.v2.views import MenuItems, Users, User, OrderItems, OrderItem, Login, PromoteUser
from app.api.v2.database import Models


def create_app(config_name):
    """creation of my app """
    app = Flask(__name__)
    api = Api(app)
    # app.config['SECRET_KEY'] = getenv('SECRET')
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    with app.app_context():
        Models().init_db()

    # version 1 routes
    api.add_resource(FoodItems, '/api/v1/orders')
    api.add_resource(FoodItem, '/api/v1/orders/<int:order_id>')
    # login routes
    api.add_resource(Login, '/api/v2/login')

    api.add_resource(OrderItems, '/api/v2/orders')
    api.add_resource(OrderItem, '/api/v2/orders/<int:order_id>')

    api.add_resource(Users, '/api/v2/users')
    api.add_resource(User, '/api/v2/users/<int:user_id>')

    api.add_resource(PromoteUser, '/api/v2/promote/<int:user_id>')

    api.add_resource(MenuItems, '/api/v2/menu')

    return app
