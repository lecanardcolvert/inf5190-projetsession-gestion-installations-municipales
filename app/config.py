import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'db/database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
