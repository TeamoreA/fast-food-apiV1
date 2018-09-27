"""Models and tokens"""
import os
from functools import wraps
from flask import jsonify, request
import jwt
import psycopg2


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
            cur.execute('SELECT * FROM users WHERE id = (%s);', (data['id'],))
            user = cur.fetchone()
            active_user = {}
            active_user['id'] = user[0]
            active_user['name'] = user[1]
            active_user['password'] = user[2]
            active_user['admin'] = user[3]

        except:
            response = jsonify({'message': 'Tokens do not match or expired!'})
            response.status_code = 401
            return response
        return f(*args, active_user, **kwargs)
    return wrapped_func
