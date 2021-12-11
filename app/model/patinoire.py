# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma
from utils.utils import parse_integer


class Patinoire(db.Model):
    __tablename__ = "patinoire"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    arrondissement = relationship("Arrondissement", backref="patinoire")
    date_heure = db.Column(db.String(19))  # Format is 'YYYY-MM-DD hh:mm:ss'
    ouvert = db.Column(db.Integer)
    deblaye = db.Column(db.Integer)
    arrose = db.Column(db.Integer)
    resurface = db.Column(db.Integer)

    def __init__(self, ice_rink_info):
        ice_rink_condition = ice_rink_info["condition"]
        last_condition = ice_rink_condition[len(ice_rink_condition) - 1]
        self.nom = ice_rink_info["nom_pat"]
        self.date_heure = last_condition["date_heure"]
        self.ouvert = parse_integer(last_condition["ouvert"])
        self.deblaye = parse_integer(last_condition["deblaye"])
        self.arrose = parse_integer(last_condition["arrose"])
        self.resurface = parse_integer(last_condition["resurface"])

    def set_arrondissement_id(self, arrondissement_id):
        self.arrondissement_id = arrondissement_id

    def get_name(self):
        return self.nom


class PatinoireModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",
            "nom",
            "arrondissement",
            "date_heure",
            "ouvert",
            "deblaye",
            "arrose",
            "resurface",
        )
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
