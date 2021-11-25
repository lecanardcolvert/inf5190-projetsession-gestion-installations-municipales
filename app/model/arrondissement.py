from sqlalchemy.orm import relationship
from utils.shared import db


class Arrondissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), unique=True, nullable=False)
    cle = db.Column(db.String(64))
    date_maj = db.Column(db.DateTime)
    installations_aquatiques = relationship(
        "InstallationAquatique", backref="arrondissement", lazy=True
    )
    patinoires = relationship("Patinoire", backref="arrondissement", lazy=True)
    glissades = relationship("Glissade", backref="arrondissement", lazy=True)

    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    def get_id(self):
        return self.id

    def set_cle(self, cle):
        self.cle = cle

    def set_date_maj(self, date_maj):
        self.date_maj = date_maj
