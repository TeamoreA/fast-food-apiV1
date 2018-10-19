"""Models and tokens"""
import re
from functools import wraps
from flask import jsonify, request

import jwt
import psycopg2
from instance.config import Config
from .datamodels import single_user_id


# conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(Config.DATABASE_URL)
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
            data = jwt.decode(token, Config.SECRET_KEY)
            user = single_user_id(data['id'])
            active_user = {}
            active_user['id'] = user[0]
            active_user['name'] = user[1]
            active_user['email'] = user[2]
            active_user['admin'] = user[4]

        except:
            response = jsonify(
                {'message': 'Invalid token, Please login to get a token!'})
            response.status_code = 401
            return response
        return f(*args, active_user, **kwargs)
    return wrapped_func


class Validators:
    """docstring for Validators"""

    def validate_name(self, name):
        """Validates the name"""
        regex = "^[a-zA-Z_ ]+$"
        return re.match(regex, name)

    def valid_email(self, email):
        """validates the user email"""
        regex = "^[^@]+@[^@]+\.[^@]+$"
        return re.match(regex, email)

    def validate_status(self, status):
        '''validator for the status field'''
        if status in ("Processing", "Complete", "Cancelled"):
            return status

    def validate_password(self, password):
        '''validate the passwoord'''
        if len(password) > 5:
            return password
