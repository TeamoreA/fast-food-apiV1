"""Models and tokens"""
import os
from functools import wraps
from flask import jsonify, request
import jwt
import psycopg2


conn = psycopg2.connect(os.getenv('DATABASE_URL'))
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
            active_user = cur.fetchone()
            # user = [user for user in USERS if user['id'] == data['id']]
            # active_user = user[0]
        except:
            response = jsonify({'message': 'Tokens do not match or expired!'})
            response.status_code = 401
            return response
        return f(active_user, *args, **kwargs)
    return wrapped_func
