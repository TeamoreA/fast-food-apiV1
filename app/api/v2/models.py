"""Models and tokens"""
import os
import re
from functools import wraps
from flask import jsonify, request
import jwt
import psycopg2
from flask import current_app
from instance.config import Config
from .datamodels import single_user_id


conn = psycopg2.connect(Config.DATABASE_URL)
# conn = psycopg2.connect(current_app.config['DATABASE_URL'])
cur = conn.cursor()


def token(f):
    """Takes in the token input"""
    @wraps(f)
    def wrapped_func(*args, **kwargs):
        """my wrapped function goes in here"""
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            response = jsonify(
                {'message': 'Ensure you are logged in to get a token!'})
            response.status_code = 401
            return response

        try:
            data = jwt.decode(token, os.getenv('SECRET'))
            user = single_user_id(data['id'])
            active_user = {}
            active_user['id'] = user[0]
            active_user['name'] = user[1]
            active_user['email'] = user[2]
            active_user['admin'] = user[3]

        except:
            response = jsonify({'message': 'Tokens do not match or expired!'})
            response.status_code = 401
            return response
        return f(*args, active_user, **kwargs)
    return wrapped_func


class Validators:
    """Validators class with regex"""

    def validate_name(self, name):
        """Validates the name"""
        regex = "^[a-zA-Z_ ]+$"
        return re.match(regex, name)

    def valid_email(self, email):
        """validates the user email"""
        regex = "^[^@]+@[^@]+\.[^@]+$"
        return re.match(regex, email)

    def validate_status(self, status):
        if status == "New" or status == "Processing" or status == "Complete":
            return status
