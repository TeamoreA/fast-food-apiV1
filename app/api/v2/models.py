"""Models and tokens"""
import os
import re
from functools import wraps
from flask import jsonify, request
import jwt
import psycopg2
from .datamodels import single_user_id


# conn = psycopg2.connect(os.getenv('DATABASE_URL'))
conn = psycopg2.connect(
    "dbname='fooddb' host= '127.0.0.1' port='5432' user='postgres' password=''")
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
            active_user['password'] = user[2]
            active_user['admin'] = user[3]

        except:
            response = jsonify({'message': 'Tokens do not match or expired!'})
            response.status_code = 401
            return response
        return f(*args, active_user, **kwargs)
    return wrapped_func


class Validators:
    """docstring for Validators"""

    def validate_name(self, name):
        """Validates the name"""
        if re.match(r"^aAzZ_ $", name):
            return name
        else:
            resp = jsonify({'message': 'Invalid name!'})
            resp.status_code = 404
            return resp

    def valid_email(self, email):
        """validates the user email"""
        if len(email) > 7:
            if re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
                return email
        resp = jsonify({'message': 'Invalid email!'})
        resp.status_code = 404
        return resp
