"""Configuration file"""
from os import getenv


class Config():
    """basic cofig class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = getenv('SECRET')
    DATABASE_URL = getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """When its under development mode"""
    DEBUG = True


class TestingConfig(Config):
    """When its under testing mode"""
    TESTING = True
    DATABASE_URL = getenv('DATABASE_TEST_URL')
    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
