"""my models to create tables"""
# import os
import psycopg2
# local imports
from instance.config import Config
from .datamodels import single_user_email, single_user_name,


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
            conn = psycopg2.connect(Config.DATABASE_URL)
            # conn = psycopg2.connect(os.getenv('DATABASE_URL'))
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

    def post_admin(self):
        """Creates a new user"""
        conn = psycopg2.connect(Config.DATABASE_URL)
        cur = conn.cursor()
        user = single_user_name(request_data['name'])
        email = single_user_email(request_data['email'])
        if not user and not email:
            cur.execute(
                "INSERT INTO\
                users (name, email, password, admin)\
                  VALUES\
                  ('Admin', 'admin@app.com', 'password', True)")
        cur.close()
        conn.commit()
