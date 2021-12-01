# Native and installed modules
import csv
import re
import traceback
import urllib3
import xmltodict
from datetime import datetime
from io import StringIO

# Custom modules
from utils.shared import db
from model.patinoire import Patinoire
from model.arrondissement import Arrondissement
from model.installation_aquatique import InstallationAquatique
from model.glissade import Glissade
from model.arrondissement import Arrondissement


def update_database():
    """Insert or update the app's database."""

    print("UPDATING DATABASE")
    try:
        arrondissements_list = {}
        arrondissements_list["last_id"] = 0
        response = fetch_data()
        ice_rink_raw_xml = response["ice_rink"].data.decode("utf-8")
        insert_ice_rinks(ice_rink_raw_xml, arrondissements_list)
        playground_slides_raw_xml = response["playground_slide"].data.decode(
            "utf-8"
        )
        insert_playground_slides(
            playground_slides_raw_xml, arrondissements_list
        )

        aquatic_installation_data = response[
            "aquatic_installation"
        ].data.decode("utf-8")
        insert_aquatic_installations(
            aquatic_installation_data, arrondissements_list
        )
        insert_arrondissements(arrondissements_list)
    except Exception:
        print(
            "Failed to parse xml from response\n(%s)" % traceback.format_exc()
        )


def fetch_data():
    """Fetch data for the app's database"""

    aquatic_installation_url = (
        "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e13615"
        "8133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/"
        "piscines.csv"
    )
    ice_rink_url = (
        "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce"
        "1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/"
        "l29-patinoire.xml"
    )
    playground_slide_url = (
        "http://www2.ville.montreal.qc.ca/services_citoyens/"
        "pdf_transfert/L29_GLISSADE.xml"
    )
    http = urllib3.PoolManager()
    playground_slide_data = http.request("GET", playground_slide_url)
    aquatic_installation_data = http.request("GET", aquatic_installation_url)
    ice_rink_data = http.request("GET", ice_rink_url)
    response = {
        "playground_slide": playground_slide_data,
        "aquatic_installation": aquatic_installation_data,
        "ice_rink": ice_rink_data,
    }
    return response


def insert_ice_rinks(ice_rink_raw_xml, arrondissements_list):
    """Insert ice rink from xml to app's database"""

    ice_rink_xml = reformat_ince_rink_xml(ice_rink_raw_xml)
    data = xmltodict.parse(ice_rink_xml, dict_constructor=dict)
    arrondissements_data = data["MAIN"]["arrondissement"]
    for arrondissement in arrondissements_data:
        nom_arr = trim_space_in_name(arrondissement["nom_arr"])
        arr_id = arrondissements_list["last_id"]
        arrondissementA = Arrondissement(id=arr_id, nom=nom_arr)
        arrondissements_list[nom_arr] = arrondissementA
        ice_rinks = arrondissement["patinoire"]
        insert_arrondissement_ice_rinks(ice_rinks, arr_id)
        arrondissements_list["last_id"] += 1


def reformat_ince_rink_xml(xml):
    """
    Reformat an ice rink xml in order to ease the parsing of an ice rink.

    This function will embed all the informations of an ice rink
    inside their own xml markup.
    The original ice rink xml is misformatted because all the ice rinks and
    their informations are put side by side and inside a single markup. So when
    we parse it raw, we can't distinguished the informations of a single ice
    rink because everything is gathered.

    Keyword arguments:
    xml -- the ice rink xml string

    return
    the xml string reformated correctly
    """

    xml = re.sub("\n", "", xml)
    xml = re.sub("> +<", "><", xml)
    xml = trim_space_in_name(xml)
    xml = re.sub(
        "</condition><nom_pat>",
        "</condition></patinoire><patinoire><nom_pat>",
        xml,
    )
    return xml


def trim_space_in_name(name):
    """Remove spaces in a name"""

    name = re.sub(" +- +", "-", name)
    name = re.sub("–", "-", name)
    return name


def insert_arrondissement_ice_rinks(ice_rinks_list, arrondissement_id):
    """Insert ice rink to app's database"""

    ice_rink_list = []
    for ice_rink in ice_rinks_list:
        nom_pat = ice_rink["nom_pat"]
        ice_rink_condition = ice_rink["condition"]
        last_condition = ice_rink_condition[len(ice_rink_condition) - 1]
        date_heure = last_condition["date_heure"]
        ouvert = parse_integer(last_condition["ouvert"])
        deblaye = parse_integer(last_condition["deblaye"])
        arrose = parse_integer(last_condition["arrose"])
        resurface = parse_integer(last_condition["resurface"])

        ice_rink = Patinoire(
            nom_pat,
            arrondissement_id,
            date_heure,
            ouvert,
            deblaye,
            arrose,
            resurface,
        )
        ice_rink_list.append(ice_rink)
    db.session.add_all(ice_rink_list)
    db.session.commit()


def parse_integer(field):
    """
    Cast field value to integer.

    if field value is None, then we return 0. We consider None as 0

    Keyword arguments:
    field -- the field that contains the value to parse

    return
    The integer obtained from the cast or 0 when field value is None
    """

    if field == "None":
        return 0
    else:
        return int(field)


def insert_playground_slides(playground_slides_raw_xml, arrondissements_list):
    """Insert playground slides into app's database"""

    playground_slides_raw = xmltodict.parse(playground_slides_raw_xml)
    playground_slides = playground_slides_raw["glissades"]["glissade"]
    playground_slide_list = []
    for playground_slide in playground_slides:
        arr_id = update_arrondissement(playground_slide, arrondissements_list)
        name = playground_slide["nom"]
        ouvert = parse_integer(playground_slide["ouvert"])
        deblaye = parse_integer(playground_slide["deblaye"])
        condition = playground_slide["condition"]
        playground_slide = Glissade(
            name,
            arr_id,
            ouvert,
            deblaye,
            condition,
        )
        playground_slide_list.append(playground_slide)
    db.session.add_all(playground_slide_list)
    db.session.commit()


def update_arrondissement(playground_slide, arrondissements_list):
    """Update arrondissement data and return its id"""

    ps_arr = playground_slide["arrondissement"]
    nom_arr_raw = ps_arr["nom_arr"]
    nom_arr = trim_space_in_name(nom_arr_raw)
    cle_arr = ps_arr["cle"]
    date_maj_arr = ps_arr["date_maj"]
    date_maj = datetime.strptime(date_maj_arr, "%Y-%m-%d %H:%M:%S")
    arr = arrondissements_list[nom_arr]
    arr.set_cle(cle_arr)
    arr.set_date_maj(date_maj)
    return arr.get_id()


def insert_aquatic_installations(
    aquatic_installation_data, arrondissements_list
):
    """Insert aquatic installation into app's database"""

    file = StringIO(aquatic_installation_data)
    data = csv.DictReader(file, delimiter=",")
    next(data)
    piscine_list = []
    for row in data:
        type = row["TYPE"]
        name = row["NOM"]
        arr_name = trim_space_in_name(row["ARRONDISSE"])
        address = row["ADRESSE"]
        property = row["PROPRIETE"]
        gestion = row["GESTION"]
        equipment = row["EQUIPEME"]
        arr_id = arrondissements_list["last_id"]
        if arrondissements_list.keys().__contains__(arr_name):
            arr = arrondissements_list[arr_name]
            arr_id: int = arr.get_id()
        else:
            arr = Arrondissement(id=arr_id, nom=arr_name)
            arrondissements_list[arr_name] = arr
            arrondissements_list["last_id"] += 1
        aquatic_installation = InstallationAquatique(arr_id, name, address)
        aquatic_installation.set_type(type)
        aquatic_installation.set_property(property)
        aquatic_installation.set_gestion(gestion)
        aquatic_installation.set_equipment(equipment)
        piscine_list.append(aquatic_installation)

    db.session.add_all(piscine_list)
    db.session.commit()


def insert_arrondissements(arrondissement_list):
    """Insert arrondissement into app's database"""

    arrondissements = []
    for key in arrondissement_list:
        if key != "last_id":
            arrondissements.append(arrondissement_list[key])

    db.session.add_all(arrondissements)
    db.session.commit()
