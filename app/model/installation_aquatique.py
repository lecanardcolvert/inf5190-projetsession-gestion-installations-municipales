from sqlalchemy import ForeignKey
from utils.shared import db


class InstallationAquatique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    adresse = db.Column(db.String(64))
    propriete = db.Column(db.String(64))
    gestion = db.Column(db.String(32))
    equipement = db.Column(db.String(32))

    def __init__(self, arrondissement_id, nom, adresse):
        self.arrondissement_id = arrondissement_id
        self.nom = nom
        self.adresse = adresse

    def set_type(self, type):
        self.type = type

    def set_property(self, propriete):
        self.propriete = propriete

    def set_gestion(self, gestion):
        self.gestion = gestion

    def set_equipment(self, equipement):
        self.equipement = equipement
