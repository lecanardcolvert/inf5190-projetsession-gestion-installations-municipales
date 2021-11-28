# Native and installed modules
from flask import Blueprint, jsonify
from utils.shared import db
import json

# Custom modules
from model.arrondissement import Arrondissement, ArrondissementModel
from model.glissade import Glissade, GlissadeModel
from model.installation_aquatique import InstallationAquatique, InstallationAquatiqueModel
from model.patinoire import Patinoire, PatinoireModel

api = Blueprint("api", __name__, url_prefix="/api")


@api.route('/installations', methods=['GET'])
def installations():
    slides = Glissade.query.all()
    slide_model = GlissadeModel(many=True)
    serialized_slides = slide_model.dump(slides)

    aquatic_installations = InstallationAquatique.query.all()
    aquatic_installations_model = InstallationAquatiqueModel(many=True)
    serialized_aquatic_installations = aquatic_installations_model.dump(aquatic_installations)

    skating_rinks = Patinoire.query.all()
    ice_rinks_model = PatinoireModel(many=True)
    serialized_ice_rinks = ice_rinks_model.dump(skating_rinks)

    return jsonify({
        'glissades': serialized_slides,
        'installations_aquatiques': serialized_aquatic_installations,
        'patinoires': serialized_ice_rinks
    })