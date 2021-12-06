# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma


class Glissade(db.Model):
    __tablename__ = 'glissade'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), unique=True, nullable=False)
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    arrondissement = relationship("Arrondissement", backref="glissade")
    ouvert = db.Column(db.Integer)
    deblaye = db.Column(db.Integer)
    condition = db.Column(db.String(32))

    def __init__(self, nom, arrondissement_id, ouvert, deblaye, condition):
        self.nom = nom
        self.arrondissement_id = arrondissement_id
        self.ouvert = ouvert
        self.deblaye = deblaye
        self.condition = condition


class GlissadeModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nom', 'arrondissement', 'ouvert', 'deblaye', 'condition')
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
