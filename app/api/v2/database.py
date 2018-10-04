"""my models to create tables"""
# import os
from os import getenv
import psycopg2

# from instance.config import Config


class Models():
    """docstring for Models"""

    def init_db(self):
        """database connection method"""
        queries = (
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                admin BOOLEAN DEFAULT FALSE
            )
            """,
            """ CREATE TABLE IF NOT EXISTS food_items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    price INTEGER NOT NULL,
                    description VARCHAR(255) 
                    )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address VARCHAR(255) NOT NULL,
                    quantity INTEGER,
                    status VARCHAR(100) DEFAULT 'New',
                    user_id INTEGER NOT NULL
            )
            """)
        conn = None
        try:
            # conn = psycopg2.connect(Config.DATABASE_URL)
            conn = psycopg2.connect(getenv('DATABASE_URI'))
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
