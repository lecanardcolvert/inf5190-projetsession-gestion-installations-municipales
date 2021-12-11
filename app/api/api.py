# Native and installed modules
from dicttoxml import dicttoxml
from flask import Blueprint, jsonify, request, Response
from sqlalchemy.orm import contains_eager
from xml.dom.minidom import parseString

# Custom modules
from model.arrondissement import Arrondissement
from model.glissade import Glissade, GlissadeModel
from model.installation_aquatique import InstallationAquatique, \
    InstallationAquatiqueModel
from model.patinoire import Patinoire, PatinoireModel

api = Blueprint("api", __name__, url_prefix="/api")


def _get_installations():
    """
    Fetches the facilities in the database and return the list.

    Returns:
    tuple -- The aquatic installations, the ice rinks, the slides
    """
    aquatic_installations = InstallationAquatique.query.all()
    ice_rinks = Patinoire.query.all()
    slides = Glissade.query.all()
    return aquatic_installations, ice_rinks, slides


@api.route('/installations', methods=['GET'])
def installations():
    """
    Return the list of facilities in the JSON format.
    Optional filter by borough using 'arrondissement' keyword arg.

    Keyword arguments:
    arrondissement -- The exact name of the borough of the facility.

    Returns:
    json -- The list of facilities in JSON format
    """
    aquatic_installations, ice_rinks, slides = _get_installations()

    arr_filter = request.args.get('arrondissement')
    if arr_filter is not None:
        slides = Glissade.query \
            .filter(Glissade.arrondissement.has(nom=arr_filter)).all()
        aquatic_installations = InstallationAquatique.query \
            .filter(
            InstallationAquatique.arrondissement.has(nom=arr_filter)).all()
        ice_rinks = Patinoire.query \
            .filter(Patinoire.arrondissement.has(nom=arr_filter)).all()

    aquatic_installation_model = InstallationAquatiqueModel(many=True)
    ice_rink_model = PatinoireModel(many=True)
    slide_model = GlissadeModel(many=True)
    serialized_aquatic = aquatic_installation_model.dump(
        aquatic_installations)
    serialized_ice_rinks = ice_rink_model.dump(ice_rinks)
    serialized_slides = slide_model.dump(slides)

    return jsonify({
        'glissades': serialized_slides,
        'installations_aquatiques': serialized_aquatic,
        'patinoires': serialized_ice_rinks
    })


def _facilities_updated_2021():
    """
    Fetches the facilities in the database. Orders them in ascending sorting
    order. Returns the list.

    Returns:
    tuple -- The aquatic installations, the ice rinks, the slides
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
    serialized_aquatic = aquatic_installation_model.dump(aquatic_installations)
    serialized_ice_rinks = ice_rink_model.dump(skating_rinks)
    serialized_slides = slide_model.dump(slides)
    return serialized_aquatic, serialized_ice_rinks, serialized_slides


@api.route('/installations-maj-2021', methods=['GET'])
def facilities_updated_2021():
    """
    Return the list of facilities updated in 2021 in the JSON format.

    Returns:
    json -- The list of facilities updated in 2021
    """
    aquatic_installations, ice_rinks, slides = _facilities_updated_2021()

    return jsonify({
        'glissades': slides,
        'installations_aquatiques': aquatic_installations,
        'patinoires': ice_rinks
    })


@api.route('/installations-maj-2021.xml', methods=['GET'])
def facilities_updated_2021_xml():
    """
    Returns the list of facilities updated in 2021 in the XML format.

    Returns:
    xml -- The list of facilities updated in 2021
    """
    aquatic_installations, ice_rinks, slides = _facilities_updated_2021()
    xml_data = [
        '<?xml version="1.0" encoding="utf-8"?><installations><glissades>',
        dicttoxml(slides, root=False, attr_type=False).decode("utf-8"),
        '</glissades><installations_aquatiques>',
        dicttoxml(aquatic_installations, root=False, attr_type=False).decode(
            "utf-8"),
        '</installations_aquatiques><patinoires>',
        dicttoxml(ice_rinks, root=False, attr_type=False).decode("utf-8"),
        '</patinoires></installations>']
    joined_xml_data = ''.join(xml_data)
    parsed_xml_data = parseString(joined_xml_data)
    pretty_xml_data = parsed_xml_data.toprettyxml()

    return Response(pretty_xml_data, mimetype='application/xml')
