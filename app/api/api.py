# Native and installed modules
from flask import Blueprint, jsonify, request

# Custom modules
from model.glissade import Glissade, GlissadeModel
from model.installation_aquatique import InstallationAquatique, InstallationAquatiqueModel
from model.patinoire import Patinoire, PatinoireModel

api = Blueprint("api", __name__, url_prefix="/api")


@api.route('/installations', methods=['GET'])
def installations():
    slides = Glissade.query.all()
    slide_model = GlissadeModel(many=True)
    aquatic_installations = InstallationAquatique.query.all()
    aquatic_installations_model = InstallationAquatiqueModel(many=True)
    skating_rinks = Patinoire.query.all()
    ice_rinks_model = PatinoireModel(many=True)

    arr_filter = request.args.get('arrondissement')
    if arr_filter is not None:
        slides = Glissade.query \
            .filter(Glissade.arrondissement.has(nom=arr_filter)).all()
        aquatic_installations = InstallationAquatique.query \
            .filter(InstallationAquatique.arrondissement.has(nom=arr_filter)).all()
        skating_rinks = Patinoire.query \
            .filter(Patinoire.arrondissement.has(nom=arr_filter)).all()

    serialized_slides = slide_model.dump(slides)
    serialized_aquatic_installations = aquatic_installations_model.dump(aquatic_installations)
    serialized_ice_rinks = ice_rinks_model.dump(skating_rinks)

    return jsonify({
        'glissades': serialized_slides,
        'installations_aquatiques': serialized_aquatic_installations,
        'patinoires': serialized_ice_rinks
    })
