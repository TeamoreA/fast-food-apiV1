""" initialise the app"""
import os
from flask import Flask
from flask_restful import Resource, Api
from instance.config import app_config
from app.api.V1.views import FoodItem, FoodItems


def create_app(config_name):
    """creation of my app """
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # version 1 routes
    api.add_resource(FoodItems, '/api/v1/orders')
    api.add_resource(FoodItem, '/api/v1/orders/<int:order_id>')

    return app
