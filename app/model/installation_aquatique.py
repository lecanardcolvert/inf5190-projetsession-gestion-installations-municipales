# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma


class InstallationAquatique(db.Model):
    __tablename__ = "installation_aquatique"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    type = db.Column(db.String(64))
    arrondissement = relationship(
        "Arrondissement", backref="installation_aquatique"
    )
    adresse = db.Column(db.String(64))
    propriete = db.Column(db.String(64))
    gestion = db.Column(db.String(32))
    equipement = db.Column(db.String(32))

    def __init__(self, aquatic_installation_info):
        self.nom = aquatic_installation_info["NOM"]
        self.adresse = aquatic_installation_info["ADRESSE"]
        self.type = aquatic_installation_info["TYPE"]
        self.propriete = aquatic_installation_info["PROPRIETE"]
        self.gestion = aquatic_installation_info["GESTION"]
        self.equipement = aquatic_installation_info["EQUIPEME"]

    def set_type(self, type):
        self.type = type

    def set_property(self, propriete):
        self.propriete = propriete

    def set_gestion(self, gestion):
        self.gestion = gestion

    def set_equipment(self, equipement):
        self.equipement = equipement

    def set_arrondissement_id(self, arrondissement_id):
        self.arrondissement_id = arrondissement_id

    def get_name(self):
        return self.nom


class InstallationAquatiqueModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",
            "nom",
            "arrondissement",
            "type",
            "adresse",
            "propriete",
            "gestion",
            "equipement",
        )
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
