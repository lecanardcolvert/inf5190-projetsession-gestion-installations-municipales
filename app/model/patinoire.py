from sqlalchemy import ForeignKey
from utils.shared import db


class Patinoire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128))
    arrondissement_id = db.Column(
        db.Integer, ForeignKey("arrondissement.id"), nullable=False
    )
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
