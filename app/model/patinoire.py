# Native and installed modules
from sqlalchemy import ForeignKey

# Custom modules
from marshmallow_sqlalchemy import fields
from model.arrondissement import ArrondissementModel
from sqlalchemy.orm import relationship
from utils.shared import db, ma


class Patinoire(db.Model):
    __tablename__ = 'patinoire'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
    arrondissement = relationship("Arrondissement", backref="patinoire")
    date_heure = db.Column(db.String(19))  # Format is 'YYYY-MM-DD hh:mm:ss'
    ouvert = db.Column(db.Integer)
    deblaye = db.Column(db.Integer)
    arrose = db.Column(db.Integer)
    resurface = db.Column(db.Integer)

    def __init__(
        self, nom, arrondissement_id, date_heure, ouvert, deblaye, arrose, resurface
    ):
        self.nom = nom
        self.arrondissement_id = arrondissement_id
        self.date_heure = date_heure
        self.ouvert = ouvert
        self.deblaye = deblaye
        self.arrose = arrose
        self.resurface = resurface


class PatinoireModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nom', 'arrondissement', 'date_heure', 'ouvert', 'deblaye', 'arrose', 'resurface')
        include_relationships = True
        ordered = True

    arrondissement = fields.Nested(ArrondissementModel)
