"""runs the app"""
from os import getenv
from app import create_app
from flask import current_app

config_name = getenv('FLASK_ENV')
app = create_app(config_name)


if __name__ == '__main__':
    app.run(debug=True)
