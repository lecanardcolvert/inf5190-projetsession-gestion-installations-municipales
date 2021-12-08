# Native and installed modules
from flask_json_schema import JsonSchema
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()
schema = JsonSchema()
