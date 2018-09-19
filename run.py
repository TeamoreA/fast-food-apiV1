"""runs the app"""
from app.api.V1.views import APP

if __name__ == '__main__':
    APP.run(debug=True)
