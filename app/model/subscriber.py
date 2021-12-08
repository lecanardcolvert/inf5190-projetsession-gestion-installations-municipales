# Native and installed modules
from sqlalchemy import JSON

# Custom modules
from utils.shared import db, ma


class Subscriber(db.Model):
    __tablename__ = 'subscriber'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    boroughs_to_follow = db.Column(JSON)

    def __init__(self, full_name, email, boroughs_to_follow):
        self.full_name = full_name
        self.email = email
        self.boroughs_to_follow = boroughs_to_follow


class SubscriberModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'full_name', 'email', 'boroughs_to_follow')
        ordered = True
