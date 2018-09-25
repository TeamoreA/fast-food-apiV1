""" initialise the app"""
import os
from flask import Flask
from flask_restful import Resource, Api
from instance.config import app_config
# from app.api.v2.views import Users, OtherUsers, Orders, OtherOrders, Login
from app.api.v1.views import OtherOrdersV1, OrdersV1
# from app.api.V1.users import Users, OtherUsers
# from app.api.V1.orders import Orders, OtherOrders
from app.api.v2.database import Models

# init_db()


def create_app(config_name):
    """creation of my app """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    Models().init_db()
    # version 1 routes
    api.add_resource(OrdersV1, '/api/v1/orders')
    api.add_resource(OtherOrdersV1, '/api/v1/orders/<int:order_id>')
    # version 2 routes
    # api.add_resource(Orders, '/api/v2/orders')
    # api.add_resource(OtherOrders, '/api/v2/orders/<int:order_id>')

    # api.add_resource(Users, '/api/v2/users')
    # api.add_resource(OtherUsers, '/api/v2/users/<user_id>')

    # api.add_resource(Login, '/api/v2/login')

    return app
