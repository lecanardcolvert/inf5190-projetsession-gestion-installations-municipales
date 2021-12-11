# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma
from utils.utils import parse_integer


class Glissade(db.Model):
    __tablename__ = "glissade"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), nullable=False)
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    arrondissement = relationship("Arrondissement", backref="glissade")
    ouvert = db.Column(db.Integer)
    deblaye = db.Column(db.Integer)
    condition = db.Column(db.String(32))

    def __init__(self, playground_slide_info):
        self.nom = playground_slide_info["nom"]
        self.ouvert = parse_integer(playground_slide_info["ouvert"])
        self.deblaye = parse_integer(playground_slide_info["deblaye"])
        self.condition = playground_slide_info["condition"]

    def set_arrondissement_id(self, arrondissement_id):
        self.arrondissement_id = arrondissement_id

    def get_name(self):
        return self.nom


class GlissadeModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = (
            "id",
            "nom",
            "arrondissement",
            "ouvert",
            "deblaye",
            "condition",
        )
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
