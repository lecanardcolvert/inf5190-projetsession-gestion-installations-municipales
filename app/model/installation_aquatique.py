from sqlalchemy import ForeignKey
from utils.shared import db


class InstallationAquatique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    type = db.Column(db.String(64))
    arrondissement_id = db.Column(db.Integer, ForeignKey('arrondissement.id'), nullable=False)
    adresse = db.Column(db.String(64))
    propriete = db.Column(db.String(64))
    gestion = db.Column(db.String(32))
    equipement = db.Column(db.String(32))