from sqlalchemy import ForeignKey
from utils.shared import db


class Glissade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    arrondissement_id = db.Column(db.Integer, ForeignKey('arrondissement.id'), nullable=False)
    ouvert = db.Column(db.Integer, 1)
    deblaye = db.Column(db.Integer, 1)
    condition = db.Column(db.String(32))