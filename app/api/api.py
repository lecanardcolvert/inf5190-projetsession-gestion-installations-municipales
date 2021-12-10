# Native and installed modules
import db
import flask
import json
import jsonschema
from dicttoxml import dicttoxml
from flask import Blueprint, jsonify, request, Response
from jsonschema import validate
from sqlalchemy import exc
from sqlalchemy.orm import contains_eager
from xml.dom.minidom import parseString

# Custom modules
from model.arrondissement import Arrondissement, ArrondissementModel
from model.glissade import Glissade, GlissadeModel
from model.installation_aquatique import InstallationAquatique, InstallationAquatiqueModel
from model.patinoire import Patinoire, PatinoireModel
from model.subscriber import Subscriber, SubscriberModel
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


def _get_installations():
    """
    Returns the list of facilities for later usage by an API.

    Return:
        The aquatic installations
        The ice rinks
        The slides
    """
    aquatic_installations = InstallationAquatique.query.all()
    ice_rinks = Patinoire.query.all()
    slides = Glissade.query.all()
    return aquatic_installations, ice_rinks, slides


@api.route('/installations', methods=['GET'])
def installations():
    """
    Returns the list of facilities in the JSON format with an optional filter by borough.

    Keyword argument:
    arrondissement -- The exact name of the borough of the facility.

    Return:
    The list of facilities in JSON format.
    """
    aquatic_installations, ice_rinks, slides = _get_installations()

    arr_filter = request.args.get('arrondissement')
    if arr_filter is not None:
        slides = Glissade.query \
            .filter(Glissade.arrondissement.has(nom=arr_filter)).all()
        aquatic_installations = InstallationAquatique.query \
            .filter(InstallationAquatique.arrondissement.has(nom=arr_filter)).all()
        ice_rinks = Patinoire.query \
            .filter(Patinoire.arrondissement.has(nom=arr_filter)).all()

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic_installations = aquatic_installation_model.dump(aquatic_installations)
    serialized_ice_rinks = ice_rink_model.dump(ice_rinks)
    serialized_slides = slide_model.dump(slides)

    return jsonify({
        'glissades': serialized_slides,
        'installations_aquatiques': serialized_aquatic_installations,
        'patinoires': serialized_ice_rinks
    })


def _facilities_updated_2021():
    """
    Returns the list of facilities updated in 2021, in ascending sorting order, for later usage by an API.

    Return:
        The aquatic installations updated in 2021, in ascending order (name)
        The ice rinks updated in 2021, in ascending order (name)
        The slides updated in 2021, in ascending order (name)
    """
    year = '2021'

    slides = Glissade.query \
        .join(Glissade.arrondissement) \
        .filter(Arrondissement.date_maj.like(year + '%')) \
        .options(contains_eager(Glissade.arrondissement)) \
        .order_by(Glissade.nom.asc()) \
        .all()
    aquatic_installations = InstallationAquatique.query \
        .join(InstallationAquatique.arrondissement) \
        .filter(Arrondissement.date_maj.like(year + '%')) \
        .options(contains_eager(InstallationAquatique.arrondissement)) \
        .order_by(InstallationAquatique.nom.asc()) \
        .all()
    skating_rinks = Patinoire.query \
        .filter(Patinoire.date_heure.contains(year)) \
        .order_by(Patinoire.nom.asc()) \
        .all()

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic_installations = aquatic_installation_model.dump(aquatic_installations)
    serialized_ice_rinks = ice_rink_model.dump(skating_rinks)
    serialized_slides = slide_model.dump(slides)
    return serialized_aquatic_installations, serialized_ice_rinks, serialized_slides


@api.route('/installations-maj-2021', methods=['GET'])
def facilities_updated_2021():
    """
    Returns the list of facilities updated in 2021 in the JSON format.

    Return:
    The list of facilities updated in 2021 in JSON format.
    """

    aquatic_installations, ice_rinks, slides = _facilities_updated_2021()

    return jsonify({
        'glissades': slides,
        'installations_aquatiques': aquatic_installations,
        'patinoires': ice_rinks
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


@api.route('/installations-maj-2021.xml', methods=['GET'])
def facilities_updated_2021_xml():
    """
    Returns the list of facilities updated in 2021 in the XML format.

    Return:
    The list of facilities updated in 2021 in XML format.
    """
    aquatic_installations, ice_rinks, slides = _facilities_updated_2021()
    xml_data = ['<?xml version="1.0" encoding="utf-8"?><installations><glissades>',
                dicttoxml(slides, root=False, attr_type=False).decode("utf-8"),
                '</glissades><installations_aquatiques>',
                dicttoxml(aquatic_installations, root=False, attr_type=False).decode("utf-8"),
                '</installations_aquatiques><patinoires>',
                dicttoxml(ice_rinks, root=False, attr_type=False).decode("utf-8"),
                '</patinoires></installations>']
    joined_xml_data = ''.join(xml_data)
    parsed_xml_data = parseString(joined_xml_data)
    pretty_xml_data = parsed_xml_data.toprettyxml()

    return Response(pretty_xml_data, mimetype='application/xml')
