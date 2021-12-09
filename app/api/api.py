# Native and installed modules
import db
import flask
import json
import jsonschema
from flask import Blueprint, jsonify, request
from jsonschema import validate

# Custom modules
from model.arrondissement import Arrondissement, ArrondissementModel
from model.subscriber import Subscriber, SubscriberModel
from model.glissade import Glissade, GlissadeModel
from model.installation_aquatique import InstallationAquatique, InstallationAquatiqueModel
from model.patinoire import Patinoire, PatinoireModel
from sqlalchemy import exc
from utils.shared import db

api = Blueprint("api", __name__, url_prefix="/api")


def _get_json_schema():
    with open('user_schema.json', 'r') as file:
        schema = json.load(file)
    return schema


def _validate_json(schema_filename, json_data):
    with open(schema_filename, 'r') as file:
        schema = json.load(file)

    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


@api.route('/installations', methods=['GET'])
def installations():
    """
    Returns the list of facilities in the JSON format, with an optional filter by borough.

    Keyword argument:
    arrondissement -- The exact name of the borough of the facility.

    Return:
    The list of facilities, in a JSON format.
    """
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


@api.route('/arrondissements', methods=['GET'])
def boroughs():
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    return jsonify(serialized_boroughs)


@api.route('/abonnement', methods=['POST'])
def subscribe():
    json_schema_path = flask.current_app.root_path + '/schemas/subscribe.json'
    request_data = request.get_json()

    if _validate_json(json_schema_path, request_data):
        subscriber = Subscriber(request_data['full_name'],
                                request_data['email'],
                                request_data['boroughs_to_follow'])

        try:
            db.session.add(subscriber)
            db.session.commit()
            subscriber_model = SubscriberModel()
            serialized_subscriber = subscriber_model.dump(subscriber)
            return jsonify(serialized_subscriber), 201
        except exc.SQLAlchemyError as err:
            return jsonify({"error": "Une erreur est survenue lors de l'ajout dans la base de données."}), 500
    else:
        return jsonify({"error": "Les données fournies ne sont pas valides."}), 400
