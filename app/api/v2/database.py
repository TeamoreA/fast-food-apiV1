"""my models to create tables"""
import os
from urllib import parse as urlparse
import psycopg2
# from urllib import parse
# from flask import jsonify


class Models():
    """docstring for Models"""

    def init_db(self):
        """database connection method"""
        queries = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                admin BOOLEAN DEFAULT FALSE
            )
            """,
            """ CREATE TABLE IF NOT EXISTS food_items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price INTEGER NOT NULL
                    )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    status VARCHAR(100) DEFAULT 'New',
                    user_id INTEGER NOT NULL
            )
            """)
        conn = None
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cur = conn.cursor()
            for query in queries:
                cur.execute(query)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            response = {"Error": error}
            print(error)
        finally:
            if conn is not None:
                conn.close()
