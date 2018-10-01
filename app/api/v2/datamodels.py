"""Database models"""
import psycopg2


conn = psycopg2.connect(
    "dbname='fooddb' host= '127.0.0.1' port='5432' user='postgres' password=''")
cur = conn.cursor()


def post_users(username, useremail, psw):
    """Creates a new user"""
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (username, useremail, psw))
    conn.commit()


def get_all_users():
    """Function gets all users"""
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    return users


def single_user_email(useremail):
    """Gets a user with a specific email"""
    cur.execute('SELECT * FROM users WHERE email = (%s);',
                (useremail,))
    user = cur.fetchone()
    return user


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


def update_user(name, hashed_pw, email, user_id):
    """Updates the user details"""
    cur.execute('UPDATE users SET name = (%s), password = (%s), email = (%s) WHERE id = (%s);',
                (name, hashed_pw, email, user_id))
    conn.commit()


def delete_user(userid):
    """Deletes a single user"""
    cur.execute('DELETE FROM users WHERE name = (%s);', (userid,))
    conn.commit()


def post_menu_items(name, price, description):
    """Creates a new user"""
    cur.execute("INSERT INTO food_items (name, price, description) VALUES (%s, %s, %s)",
                (name, price, description))
    conn.commit()


def single_menu_name(menuname):
    """Gets a user with a specific name"""
    cur.execute('SELECT * FROM food_items WHERE name = (%s);',
                (menuname,))
    food_item = cur.fetchone()
    return food_item


def get_all_menuitems():
    """gets all menu items"""
    cur.execute('SELECT * FROM food_items;')
    orders = cur.fetchall()
    return orders


def get_all_orders():
    """gets all orders"""
    cur.execute('SELECT * FROM orders;')
    orders = cur.fetchall()
    return orders


def post_order_item(name, user_id):
    """creates a new order"""
    cur.execute("INSERT INTO orders (name, user_id) VALUES (%s, %s)",
                (name, user_id))
    conn.commit()


def check_user_orders(order_id):
    """Checks orders of a specific user"""
    cur.execute('SELECT * FROM orders WHERE user_id = (%s);', (order_id,))
    orders = cur.fetchall()
    return orders


def single_order_id(order_id):
    """selects specific orders"""
    cur.execute('SELECT * FROM orders WHERE id = (%s);', (order_id,))
    order = cur.fetchone()
    return order


def update_order(status, order_id):
    """Updates an order"""
    cur.execute('UPDATE orders SET status = (%s) WHERE id = (%s);',
                (status, order_id))
    conn.commit()


def single_order_user_id(name, user_id):
    """matching user with the orders"""
    cur.execute('SELECT * FROM orders WHERE name = (%s) AND user_id = (%s);',
                (name, user_id))
    order = cur.fetchone()
    return order


def delete_order(order_id):
    """delete an order"""
    cur.execute('DELETE FROM orders WHERE id = (%s);', (order_id,))
    conn.commit()
