# Native and installed modules
import flask
import json
import jsonschema
from dicttoxml import dicttoxml
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from flask import Blueprint, jsonify, request, Response
from sqlalchemy import exc
from sqlalchemy.orm import contains_eager
from xml.dom.minidom import parseString

# Custom modules
from model.arrondissement import Arrondissement, ArrondissementModel
from model.installation_aquatique import (
    InstallationAquatique,
    InstallationAquatiqueModel,
)
from model.glissade import Glissade, GlissadeModel
from model.patinoire import Patinoire, PatinoireModel
from model.subscriber import Subscriber, SubscriberModel
from schemas.schemas import update_playground_slide_schema
from utils.shared import db

api = Blueprint("api", __name__, url_prefix="/api/v1")
playground_slide_schema = GlissadeModel()


def _get_json_schema():
    """
    Open a json schema file, and return the data.
    Returns:
    object -- The object containing the json data
    """
    with open("user_schema.json", "r") as file:
        schema = json.load(file)
    return schema


def _get_all_facilities():
    """
    Fetch the facilities in the database and return the list.

    Returns:
    tuple -- The aquatic facilities, the ice rinks, the slides
    """
    aquatic_facilities = InstallationAquatique.query.all()
    ice_rinks = Patinoire.query.all()
    slides = Glissade.query.all()
    return aquatic_facilities, ice_rinks, slides


def _get_facilities_updated_2021():
    """
    Fetch the facilities in the database. Orders them in ascending sorting
    order. Return the list.

    Returns:
    tuple -- The aquatic facilities, the ice rinks, the slides
    """
    year = "2021"

    slides = (
        Glissade.query.join(Glissade.arrondissement)
        .filter(Arrondissement.date_maj.like(year + "%"))
        .options(contains_eager(Glissade.arrondissement))
        .order_by(Glissade.nom.asc())
        .all()
    )
    aquatic_facilities = (
        InstallationAquatique.query.join(InstallationAquatique.arrondissement)
        .filter(Arrondissement.date_maj.like(year + "%"))
        .options(contains_eager(InstallationAquatique.arrondissement))
        .order_by(InstallationAquatique.nom.asc())
        .all()
    )
    skating_rinks = (
        Patinoire.query.filter(Patinoire.date_heure.contains(year))
        .order_by(Patinoire.nom.asc())
        .all()
    )

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic = aquatic_installation_model.dump(aquatic_facilities)
    serialized_ice_rinks = ice_rink_model.dump(skating_rinks)
    serialized_slides = slide_model.dump(slides)

    return serialized_aquatic, serialized_ice_rinks, serialized_slides


def _validate_json(schema_filename, json_data):
    """
    Validate json data using a schema.

    Keyword arguments:
    schema_filename -- The path of the schema.
    json_data -- The json data to validate.

    Returns:
    bool -- True if the json data is valid, else false.
    """
    with open(schema_filename, "r") as file:
        schema = json.load(file)

    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


# TODO: not working for now
# def validate_schema(schema):
#     """
#     Decorator for validating request using schema
#
#     Keyword arguments:
#     schema -- The schema which will be used to validate request
#     """
#
#     def inner_function(f):
#         @wraps(f)
#         def decorated(*args, **kwargs):
#             validate(instance=request.json, schema=schema)
#             f(*args, **kwargs)
#
#         return decorated
#
#     return inner_function


@api.app_errorhandler(ValidationError)
def give_validation_error(e):
    """Give an error response when request validation fails."""

    return (
        jsonify({"error": {"code": "Bad Request", "message": e.message}}),
        400,
    )


@api.route("/abonnement", methods=["POST"])
def subscribe():
    """
    Insert a new subscriber in the database.

    Keyword arguments:
    full_name -- The full name of the subscriber
    email -- The email of the subscriber
    boroughs_to_follow - An array containing the boroughs id

    Returns:
    json -- The subscriber data when no errors are found
    json -- An error when a problem is detected in the data submitted
    json -- An error when a problem is detected when adding data to database
    """
    json_schema_path = flask.current_app.root_path + "/schemas/subscribe.json"
    request_data = request.get_json()

    if _validate_json(json_schema_path, request_data):
        subscriber = Subscriber(
            request_data["full_name"],
            request_data["email"],
            request_data["boroughs_to_follow"],
        )

        try:
            db.session.add(subscriber)
            db.session.commit()
            subscriber_model = SubscriberModel()
            serialized_subscriber = subscriber_model.dump(subscriber)
            return jsonify(serialized_subscriber), 201
        except exc.SQLAlchemyError as err:
            return (
                jsonify(
                    {
                        "error": "Une erreur est survenue lors de l'ajout dans"
                        " la base de données."
                    }
                ),
                500,
            )

    else:
        return (
            jsonify({"error": "Les données fournies ne sont pas valides."}),
            400,
        )


@api.route("/arrondissements", methods=["GET"])
def boroughs():
    """
    Fetch the boroughs in the database, then returns the list in json format.

    Returns:
    json -- The list of boroughs in json format
    """
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    return jsonify(serialized_boroughs)


@api.route("/installations", methods=["GET"])
def facilities():
    """
    Return the list of facilities in the json format.
    Optional filter by borough using 'arrondissement' keyword arg.

    Keyword arguments:
    arrondissement -- The exact name of the borough of the facility.

    Returns:
    json -- The list of facilities in JSON format
    """
    aquatic_facilities, ice_rinks, slides = _get_all_facilities()
    arr_filter = request.args.get("arrondissement")
    if arr_filter is not None:
        slides = Glissade.query.filter(
            Glissade.arrondissement.has(nom=arr_filter)
        ).all()
        aquatic_facilities = InstallationAquatique.query.filter(
            InstallationAquatique.arrondissement.has(nom=arr_filter)
        ).all()
        ice_rinks = Patinoire.query.filter(
            Patinoire.arrondissement.has(nom=arr_filter)
        ).all()

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic = aquatic_installation_model.dump(aquatic_facilities)
    serialized_ice_rinks = ice_rink_model.dump(ice_rinks)
    serialized_slides = slide_model.dump(slides)

    return jsonify(
        {
            "glissades": serialized_slides,
            "installations_aquatiques": serialized_aquatic,
            "patinoires": serialized_ice_rinks,
        }
    )


@api.route("/installations-maj-2021", methods=["GET"])
def facilities_updated_2021():
    """
    Return the list of facilities updated in 2021 in the json format.

    Returns:
    json -- The list of facilities updated in 2021
    """
    aquatic_facilities, ice_rinks, slides = _get_facilities_updated_2021()
    return jsonify(
        {
            "glissades": slides,
            "installations_aquatiques": aquatic_facilities,
            "patinoires": ice_rinks,
        }
    )


@api.route("/installations-maj-2021.xml", methods=["GET"])
def facilities_updated_2021_xml():
    """
    Return the list of facilities updated in 2021 in the xml format.

    Returns:
    xml -- The list of facilities updated in 2021
    """
    aquatic_facilities, ice_rinks, slides = _get_facilities_updated_2021()
    xml_data = [
        '<?xml version="1.0" encoding="utf-8"?><installations><glissades>',
        dicttoxml(slides, root=False, attr_type=False).decode("utf-8"),
        "</glissades><installations_aquatiques>",
        dicttoxml(aquatic_facilities, root=False, attr_type=False).decode(
            "utf-8"
        ),
        "</installations_aquatiques><patinoires>",
        dicttoxml(ice_rinks, root=False, attr_type=False).decode("utf-8"),
        "</patinoires></installations>",
    ]
    joined_xml_data = "".join(xml_data)
    parsed_xml_data = parseString(joined_xml_data)
    pretty_xml_data = parsed_xml_data.toprettyxml()

    return Response(pretty_xml_data, mimetype="application/xml")


@api.route("/installations-noms", methods=["GET"])
def facility_names():
    """
    Return the list of facility names in the json format, in alphabetical
    order.

    Returns:
    json -- The list of facility names in json format
    """
    aquatic_facilities, ice_rinks, slides = _get_all_facilities()
    facility_names = []
    for aquatic_facility in aquatic_facilities:
        facility_names.append(aquatic_facility.nom)
    for ice_rink in ice_rinks:
        facility_names.append(ice_rink.nom)
    for slide in slides:
        facility_names.append(slide.nom)
    sorted_facility_names = sorted(facility_names)

    return jsonify(sorted_facility_names)


@api.route("/installations-recherche-nom", methods=["GET"])
def facility_name_search():
    """
    Return the list of facilities in the json format.
    Optional filter by borough using 'nom' keyword arg.

    Keyword arguments:
    name -- The exact name of the facility to look for.

    Returns:
    json -- The list of facilities in json format
    """
    name_filter = request.args.get("nom")
    if name_filter is not None:
        slides = Glissade.query.filter(Glissade.nom == name_filter).all()
        aquatic_facilities = InstallationAquatique.query.filter(
            InstallationAquatique.nom == name_filter
        ).all()
        ice_rinks = Patinoire.query.filter(Patinoire.nom == name_filter).all()

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic = aquatic_installation_model.dump(aquatic_facilities)
    serialized_ice_rinks = ice_rink_model.dump(ice_rinks)
    serialized_slides = slide_model.dump(slides)

    return jsonify(
        {
            "glissades": serialized_slides,
            "installations_aquatiques": serialized_aquatic,
            "patinoires": serialized_ice_rinks,
        }
    )


@api.route("/installations/glissades/<id>", methods=["PUT"])
# @validate_schema(update_playground_slide_schema)
def update_playground_slide(id):
    """
    Update a playground_slide
    keyword arguments:
    id -- the id of the playground slide
    """

    query = Glissade.query.filter(Glissade.id == id)
    result = query.first()
    if result is None:
        return (
            jsonify(
                {
                    "error": {
                        "code": "Not Found",
                        "message": "Can't find this playground_slide",
                    }
                }
            ),
            404,
        )
    else:
        validate(instance=request.json, schema=update_playground_slide_schema)
        playground_slide = Glissade.query.get(id)
        playground_slide.nom = request.json["nom"]
        playground_slide.arrondissement_id = request.json["arrondissement_id"]
        playground_slide.ouvert = request.json["ouvert"]
        playground_slide.deblaye = request.json["deblaye"]
        playground_slide.condition = request.json["condition"]
        db.session.commit()
        return playground_slide_schema.jsonify(playground_slide), 200
