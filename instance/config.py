"""Configuration file"""
import os


class Config(object):
    """basic cofig class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    DATABASE_URL = os.getenv('DATABASE_URI')


class ProductionConfig(Config):
    """When its under production mode"""
    TESTING = False
    DEBUG = False


class DevelopmentConfig(Config):
    """When its under development mode"""
    DEBUG = True


class TestingConfig(Config):
    """When its under testing mode"""
    TESTING = True
    DATABASE_URL = "dbname='fooddb' host='127.0.0.1' port='5432' user='postgres' password=''"
    DEBUG = True

app_config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
