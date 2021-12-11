# Native and installed modules
import json
import jsonschema
from dicttoxml import dicttoxml
from jsonschema import validate
from flask import Blueprint, jsonify, request, Response, current_app
from sqlalchemy import exc
from sqlalchemy.orm import contains_eager
from xml.dom.minidom import parseString

# Custom modules
from model.arrondissement import Arrondissement, ArrondissementModel
from model.installation_aquatique import (
    InstallationAquatique,
    InstallationAquatiqueModel,
)
from model.subscriber import Subscriber, SubscriberModel
from model.glissade import Glissade, GlissadeModel
from model.patinoire import Patinoire, PatinoireModel
from utils.shared import db

api = Blueprint("api", __name__, url_prefix="/api")


def _get_facilities():
    """
    Fetch the facilities in the database and return the list.

    Returns:
    tuple -- The aquatic facilities, the ice rinks, the slides
    """
    aquatic_facilities = InstallationAquatique.query.all()
    ice_rinks = Patinoire.query.all()
    slides = Glissade.query.all()
    return aquatic_facilities, ice_rinks, slides


def _get_json_schema():
    """
    Open a json schema file, and return the data.

    Returns:
    object -- The object containing the json data
    """
    with open("user_schema.json", "r") as file:
        schema = json.load(file)
    return schema


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


@api.route("/installations", methods=["GET"])
def facilities():
    """
    Return the list of facilities in the JSON format.
    Optional filter by borough using 'arrondissement' keyword arg.

    Keyword arguments:
    arrondissement -- The exact name of the borough of the facility.

    Returns:
    json -- The list of facilities in JSON format
    """
    aquatic_facilities, ice_rinks, slides = _get_facilities()
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


def _facilities_updated_2021():
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


@api.route("/installations-maj-2021", methods=["GET"])
def facilities_updated_2021():
    """
    Return the list of facilities updated in 2021 in the json format.

    Returns:
    json -- The list of facilities updated in 2021
    """
    aquatic_facilities, ice_rinks, slides = _facilities_updated_2021()
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
    aquatic_facilities, ice_rinks, slides = _facilities_updated_2021()
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
    json_schema_path = current_app.root_path + "/schemas/subscribe.json"
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
