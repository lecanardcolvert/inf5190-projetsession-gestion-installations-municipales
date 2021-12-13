import os
import yaml

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "db/database.db")
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.yml")

with open(CONFIG_FILE_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

# Twitter config
TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Mail config
mail = config["mail"]
RECIPIENT = mail["recipient"]
SUBJECT = mail["subject"]
USER_MAIL = os.environ.get("INF5190_SERVER_MAIL")
MAIL_PASSWORD = os.environ.get("INF5190_MAIL_SERVER_PASSWORD")

# Basic Auth
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    """Add dev environment config here"""


class TestConfig(Config):
    """Add test environment config here"""


class ProductionConfig(Config):
    """Add production environment config here"""


config = {
    "development": DevelopmentConfig,
    "testing": TestConfig,
    "production": ProductionConfig,
}
