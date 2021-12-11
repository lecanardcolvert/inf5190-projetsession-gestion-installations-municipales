# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma


class InstallationAquatique(db.Model):
    __tablename__ = 'installation_aquatique'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    type = db.Column(db.String(64))
    arrondissement = relationship("Arrondissement", backref="installation_aquatique")
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


class InstallationAquatiqueModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nom', 'arrondissement', 'type', 'adresse', 'propriete', 'gestion', 'equipement')
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
