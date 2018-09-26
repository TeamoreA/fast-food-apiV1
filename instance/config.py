"""Configuration file"""
import os


class Config():
    """basic cofig class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """When its under development mode"""
    DEBUG = True


class TestingConfig(Config):
    """When its under testing mode"""
    TESTING = True
    DATABASE_URI = "dbname='db1' host= '127.0.0.1' port='5432' user='postgres' password=''"
    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
