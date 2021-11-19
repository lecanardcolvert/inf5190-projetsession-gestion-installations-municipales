from sqlalchemy.orm import relationship
from utils.shared import db


class Arrondissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), unique=True)
    cle = db.Column(db.String(64))
    dateMaj = db.Column(db.DateTime)
    glissades = relationship('Glissade', backref='arrondissement', lazy=True)
    installations_aquatiques = relationship('InstallationAquatique', backref='arrondissement', lazy=True)
    patinoires = relationship('Patinoire', backref='arrondissement', lazy=True)