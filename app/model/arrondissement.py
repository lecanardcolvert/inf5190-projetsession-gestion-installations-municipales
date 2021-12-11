# Custom modules
from utils.shared import db, ma


class Arrondissement(db.Model):
    __tablename__ = 'arrondissement'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(128), unique=True, nullable=False)
    cle = db.Column(db.String(64))
    date_maj = db.Column(db.DateTime)

    def __init__(self, id, nom):
        self.id = id
        self.nom = nom

    def get_id(self):
        return self.id

    def set_cle(self, cle):
        self.cle = cle

    def set_date_maj(self, date_maj):
        self.date_maj = date_maj


class ArrondissementModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'nom', 'cle', 'date_maj')
        ordered = True
