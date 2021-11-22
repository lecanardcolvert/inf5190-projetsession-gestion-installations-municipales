import traceback
from datetime import datetime
import re
import urllib3
import xmltodict
import csv
from io import StringIO

from utils.shared import db
from model.patinoire import Patinoire
from model.arrondissement import Arrondissement
from model.installation_aquatique import InstallationAquatique
from model.glissade import Glissade
from model.arrondissement import Arrondissement


def update_database():
    try:
        response = fetch_data()
        data = xmltodict.parse(response["glissade"].data)
        #    print(data["glissades"]["glissade"][0]["nom"])

        #   print("--------------AQUATIQUE----------------")
        content = response["aquatic_installation"].data.decode()
        file = StringIO(content)
        data = csv.reader(file, delimiter=",")
        next(data)
        row1 = next(data)
        #  print(row1)
        # for row in data:
        #    print(row[3])
        # content2 = [line.decode("utf-8") for line in response2.data.readlines()]

        print("--------------PATINOIRE----------------")
        xml = response["patinoire"].data.decode("utf-8")
        xml = re.sub("\n", "", xml)
        xml = re.sub("> +<", "><", xml)
        xml = re.sub(
            "</condition><nom_pat>",
            "</condition></patinoire><patinoire><nom_pat>",
            xml,
        )
        data = xmltodict.parse(xml, dict_constructor=dict)
        arrondissements = data["MAIN"]["arrondissement"]
        arrondissement_id = 0
        arrondissements_list = []
        for arrondissement in arrondissements:
            nom_arr = arrondissement["nom_arr"]
            date_en_iso = datetime.strptime(
                "31 December 2020", "%d %B %Y"
            ).date()
            arrondissementA = Arrondissement(
                id=arrondissement_id, nom=nom_arr, dateMaj=date_en_iso
            )
            arrondissements_list.append(arrondissementA)

            patinoires = arrondissement["patinoire"]
            insert_patinoires(patinoires, arrondissement_id)
            arrondissement_id += 1
        db.session.add_all(arrondissements_list)
        db.session.commit()

    except Exception:
        print(
            "Failed to parse xml from response (%s)" % traceback.format_exc()
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


def insert_patinoires(patinoires_list, arrondissement_id):
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
    """Cast field value to integer.
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
