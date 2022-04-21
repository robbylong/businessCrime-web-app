"""Flask config class."""
from pathlib import Path


class Config(object):
    DEBUG = False
    SECRET_KEY = 'roHlg3hxP6Pw7hHOn6pm6w'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = Path('data')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('crime_app.sqlite'))
    UPLOADED_PHOTOS_DEST = Path(__file__).parent.joinpath("static/img")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    ENV = 'development'
    SQLALCHEMY_ECHO = False
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    #  False for testing but turn to True if you want to echo SQL to the console for debugging database queries
    SQLALCHEMY_ECHO = False
    #  Tests will fail without this. This allows forms to be submitted from the tests without the CSRF token
    WTF_CSRF_ENABLED = False
