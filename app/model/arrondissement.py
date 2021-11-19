from utils.shared import db


class Arrondissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True)
    cle = db.Column(db.String(50))
    dateMaj = db.Column(db.DateTime)
