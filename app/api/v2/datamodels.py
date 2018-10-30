"""Database models"""
from os import getenv
import psycopg2
# local imports
from instance.config import Config
conn = psycopg2.connect(Config.DATABASE_URL)
# cur = conn.cursor()


def post_users(username, useremail, psw):
    """Creates a new user"""
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (username, useremail, psw))
    cur.close()
    conn.commit()


def get_all_users():
    """gets all users"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    return users


def single_user_name(username):
    """Gets a user with a specific name"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE name = (%s);',
                (username,))
    user = cur.fetchone()
    cur.close()
    return user


def single_user_email(email):
    """Gets a user with a specific name"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE email = (%s);',
                (email,))
    user = cur.fetchone()
    cur.close()
    return user


def single_user_id(userid):
    """gets a user with a specific id"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = (%s);',
                (userid,))
    user = cur.fetchone()
    cur.close()
    return user


def promote_user(userid):
    """promotes a user to an admin"""
    cur = conn.cursor()
    cur.execute('UPDATE users SET admin = (%s) WHERE id = (%s);',
                (True, userid))
    cur.close()
    conn.commit()


def update_user(name, hashed_pw, email, user_id):
    """Updates the user details"""
    cur = conn.cursor()
    cur.execute('UPDATE users SET name = (%s), password = (%s), email = (%s) WHERE id = (%s);',
                (name, hashed_pw, email, user_id))
    cur.close()
    conn.commit()


def delete_user(userid):
    """Deletes a single user"""
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE name = (%s);', (userid,))
    cur.close()
    conn.commit()


def post_menu_items(name, price, description, image):
    """Creates a new user"""
    cur = conn.cursor()
    cur.execute("INSERT INTO food_items (name, price, description, image) VALUES (%s, %s, %s, %s)",
                (name, price, description, image))
    cur.close()
    conn.commit()


def single_menu_name(menuname):
    """Gets a user with a specific name"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM food_items WHERE name = (%s);',
                (menuname,))
    food_item = cur.fetchone()
    return food_item


def get_all_menuitems():
    """gets all menu items"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM food_items;')
    orders = cur.fetchall()
    cur.close()
    return orders


def get_all_orders():
    """gets all orders"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders;')
    orders = cur.fetchall()
    cur.close()
    return orders


def post_order_item(name, address, quantity, user_id):
    """creates a new order"""
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (name,address,quantity, user_id) VALUES (%s,%s,%s, %s)",
                (name, address, quantity, user_id))
    cur.close()
    conn.commit()


def check_user_orders(order_id):
    """Checks orders of a specific user"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE user_id = (%s);', (order_id,))
    orders = cur.fetchall()
    cur.close()
    return orders


def single_order_id(order_id):
    """selects specific orders"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM orders WHERE id = (%s);', (order_id,))
    order = cur.fetchone()
    cur.close()
    return order


def single_menu_id(menu_id):
    """selects specific menu item"""
    cur = conn.cursor()
    cur.execute('SELECT * FROM food_items WHERE id = (%s);', (menu_id,))
    menu_item = cur.fetchone()
    cur.close()
    return menu_item


def update_order(status, order_id):
    """Updates an order"""
    cur = conn.cursor()
    cur.execute('UPDATE orders SET status = (%s) WHERE id = (%s);',
                (status, order_id))
    cur.close()
    conn.commit()


def delete_order(order_id):
    """delete an order"""
    cur = conn.cursor()
    cur.execute('DELETE FROM orders WHERE id = (%s);', (order_id,))
    cur.close()
    conn.commit()


def delete_menu(menu_id):
    """delete a menu item"""
    cur = conn.cursor()
    cur.execute('DELETE FROM food_items WHERE id = (%s);', (menu_id,))
    cur.close()
    conn.commit()


def drop_tables():
    """delete an order"""
    cur = conn.cursor()
    cur.execute('DROP TABLE users, orders, food_items;')
    cur.close()
    conn.commit()

# conn.close()
