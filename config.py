import os

POSTGRES = {
    "user": "postgres",
    "pw" : "postgres",
    "db" : "journal",
    "host" : "localhost",
    "port" : "5432"
}

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-shall-not-pass'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(**POSTGRES)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
"""