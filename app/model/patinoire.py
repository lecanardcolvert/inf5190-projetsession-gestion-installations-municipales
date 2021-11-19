from sqlalchemy import ForeignKey
from utils.shared import db


class Patinoire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    arrondissement_id = db.Column(db.Integer, ForeignKey('arrondissement.id'), nullable=False)
    dateMaj = db.Column(db.String(19))  # Format is 'YYYY-MM-DD hh:mm:ss'
    ouvert = db.Column(db.Integer, 1)
    deblaye = db.Column(db.Integer, 1)
    arrose = db.Column(db.Integer, 1)
    resurface = db.Column(db.Integer, 1)