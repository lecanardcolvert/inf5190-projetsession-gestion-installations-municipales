# Native and installed modules
import difflib
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
    try:
        arrondissements_list = {}
        response = fetch_data()

        # print("--------------PATINOIRE----------------")
        ice_rink_raw_xml = response["patinoire"].data.decode("utf-8")
        ice_rink_xml = reformat_ince_rink_xml(ice_rink_raw_xml)
        data = xmltodict.parse(ice_rink_xml, dict_constructor=dict)

        arrondissements = data["MAIN"]["arrondissement"]
        arrondissement_id = 0

        for arrondissement in arrondissements:
            nom_arr = trim_space_in_name(arrondissement["nom_arr"])
            arrondissementA = Arrondissement(id=arrondissement_id, nom=nom_arr)
            arrondissements_list[nom_arr] = arrondissementA

            patinoires = arrondissement["patinoire"]
            insert_patinoires(patinoires, arrondissement_id)
            arrondissement_id += 1

        # TODO: insert playground slide
        # print("--------------GLISSADE / playground slide ----------------")
        data = xmltodict.parse(response["glissade"].data)
        playground_slides = data["glissades"]["glissade"]

        glissade_list = []
        for playground_slide in playground_slides:
            ps_arr = playground_slide["arrondissement"]
            nom_arr_raw = ps_arr["nom_arr"]
            nom_arr = trim_space_in_name(nom_arr_raw)
            cle_arr = ps_arr["cle"]
            date_maj_arr = ps_arr["date_maj"]
            date_maj = datetime.strptime(date_maj_arr, "%Y-%m-%d %H:%M:%S")
            arr = arrondissements_list[nom_arr]
            arr.set_cle(cle_arr)
            arr.set_date_maj(date_maj)
            arr_id: int = arr.get_id()

            glissade_name = playground_slide["nom"]
            glissade_ouvert = parse_integer(playground_slide["ouvert"])
            glissade_deblaye = parse_integer(playground_slide["deblaye"])
            glissade_condition = playground_slide["condition"]

            glissade = Glissade(
                glissade_name,
                arr_id,
                glissade_ouvert,
                glissade_deblaye,
                glissade_condition,
            )
            glissade_list.append(glissade)

        db.session.add_all(glissade_list)
        db.session.commit()

        # insert aquatic_installation
        #   print("--------------AQUATIQUE----------------")
        content = response["aquatic_installation"].data.decode("utf-8")
        file = StringIO(content)
        data = csv.DictReader(file, delimiter=",")
        next(data)
        # for key in arrondissements_list:
        #     print(f"Nom => {key}")
        piscine_list = []
        for row in data:
            type = row["TYPE"]
            name = row["NOM"]
            arr_name = trim_space_in_name(row["ARRONDISSE"])
            address = row["ADRESSE"]
            property = row["PROPRIETE"]
            gestion = row["GESTION"]
            equipment = row["EQUIPEME"]
            # print("############")
            # print(arrondissements_list.keys())
            arr_id = arrondissement_id
            if arrondissements_list.keys().__contains__(arr_name):
                arr = arrondissements_list[arr_name]
                arr_id: int = arr.get_id()
            else:
                arr = Arrondissement(id=arrondissement_id, nom=arr_name)
                arrondissements_list[arr_name] = arr
                arrondissement_id += 1
            # print("############")
            aquatic_installation = InstallationAquatique(arr_id, name, address)
            aquatic_installation.set_type(type)
            aquatic_installation.set_property(property)
            aquatic_installation.set_gestion(gestion)
            aquatic_installation.set_equipment(equipment)
            piscine_list.append(aquatic_installation)

        db.session.add_all(piscine_list)
        db.session.commit()
        # content2 = [
        #     line.decode("utf-8") for line in response2.data.readlines()
        # ]
        # print(content2)

        # Insert all arrondissements
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
    patinoire_url = (
        "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce"
        "1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/"
        "l29-patinoire.xml"
    )
    glissade_url = (
        "http://www2.ville.montreal.qc.ca/services_citoyens/"
        "pdf_transfert/L29_GLISSADE.xml"
    )
    http = urllib3.PoolManager()
    glissade_data = http.request("GET", glissade_url)
    aquatic_installation_data = http.request("GET", aquatic_installation_url)
    patinoire_data = http.request("GET", patinoire_url)
    response = {
        "glissade": glissade_data,
        "aquatic_installation": aquatic_installation_data,
        "patinoire": patinoire_data,
    }
    return response


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


def insert_patinoires(patinoires_list, arrondissement_id):
    """Insert patinoire to app's database"""

    patinoire_list = []
    for patinoire in patinoires_list:
        nom_pat = patinoire["nom_pat"]
        patinoire_condition = patinoire["condition"]
        last_condition = patinoire_condition[len(patinoire_condition) - 1]
        date_heure = last_condition["date_heure"]
        ouvert = parse_integer(last_condition["ouvert"])
        deblaye = parse_integer(last_condition["deblaye"])
        arrose = parse_integer(last_condition["arrose"])
        resurface = parse_integer(last_condition["resurface"])

        patinoire = Patinoire(
            nom_pat,
            arrondissement_id,
            date_heure,
            ouvert,
            deblaye,
            arrose,
            resurface,
        )
        patinoire_list.append(patinoire)
    db.session.add_all(patinoire_list)
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


def insert_arrondissements(arrondissement_list):
    """Insert arrondissement into app's database"""

    arrondissements = []
    for key in arrondissement_list:
        arrondissements.append(arrondissement_list[key])

    db.session.add_all(arrondissements)
    db.session.commit()
