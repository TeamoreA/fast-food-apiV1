""" initialise the app"""
import os
from flask import Flask, redirect
from flask_restful import Resource, Api
from instance.config import app_config
from app.api.V1.views import FoodItem, FoodItems
from app.api.v2.views import MenuItems, Users, SingleUser, OrderItems,\
    OrderItem, Login, PromoteUser, UserOrders, SingleMenu
from app.api.v2.database import Models


def create_app(config_name):
    """creation of my app """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    # app.config['SECRET_KEY'] = os.getenv('SECRET')
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    with app.app_context():
        Models().init_db()
        Models().post_admin()

    # version 1 routes
    api.add_resource(FoodItems, '/api/v1/orders')
    api.add_resource(FoodItem, '/api/v1/orders/<int:order_id>')
    # login routes
    api.add_resource(Login, '/api/v2/auth/signin')

    api.add_resource(OrderItems, '/api/v2/orders')
    api.add_resource(OrderItem, '/api/v2/orders/<int:order_id>')

    api.add_resource(UserOrders, '/api/v2/users/orders/<int:user_id>')

    api.add_resource(Users, '/api/v2/auth/signup')
    api.add_resource(SingleUser, '/api/v2/auth/users/<int:user_id>')

    api.add_resource(PromoteUser, '/api/v2/promote/<int:user_id>')

    api.add_resource(MenuItems, '/api/v2/menu')
    api.add_resource(SingleMenu, '/api/v2/menu/<int:menu_id>')

    # redirect
    @app.route('/')
    def index():
        return redirect('https://foodapi11.docs.apiary.io/#')

    return app
