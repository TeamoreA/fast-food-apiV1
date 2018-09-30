"""Database models"""
import psycopg2


conn = psycopg2.connect(
    "dbname='fooddb' host= '127.0.0.1' port='5432' user='postgres' password=''")
cur = conn.cursor()


def post_users(username, psw):
    """Creates a new user"""
    cur.execute("INSERT INTO users (name, password) VALUES (%s, %s)",
                (username, psw))
    conn.commit()


def get_all_users():
    """Function gets all users"""
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    return users


def single_user_name(username):
    """Gets a user with a specific name"""
    cur.execute('SELECT * FROM users WHERE name = (%s);',
                (username,))
    user = cur.fetchone()
    return user


def single_user_id(userid):
    """gets a user with a specific id"""
    cur.execute('SELECT * FROM users WHERE id = (%s);',
                (userid,))
    user = cur.fetchone()
    return user


def promote_user(userid):
    """promotes a user to an admin"""
    cur.execute('UPDATE users SET admin = (%s) WHERE id = (%s);',
                (True, userid))
    conn.commit()


def update_user(name, hashed_pw, user_id):
    """Updates the user details"""
    cur.execute('UPDATE users SET name = (%s), password = (%s) WHERE id = (%s);',
                (name, hashed_pw, user_id))
    conn.commit()


def delete_user(userid):
    """Deletes a single user"""
    cur.execute('DELETE FROM users WHERE name = (%s);', (userid,))
    conn.commit()


def post_menu_items(name, price):
    """Creates a new user"""
    cur.execute("INSERT INTO food_items (name, price) VALUES (%s, %s)",
                (name, price))
    conn.commit()


def single_menu_name(menuname):
    """Gets a user with a specific name"""
    cur.execute('SELECT * FROM food_items WHERE name = (%s);',
                (menuname,))
    food_item = cur.fetchone()
    return food_item


def get_all_menuitems():
    cur.execute('SELECT * FROM food_items;')
    orders = cur.fetchall()
    return orders


def get_all_orders():
    cur.execute('SELECT * FROM orders;')
    orders = cur.fetchall()
    return orders
