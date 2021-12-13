# Native and installed modules
import csv
import traceback
import urllib3
import xmltodict
from datetime import datetime
from io import StringIO

# Custom modules
import config
from flask import g, render_template
from model.glissade import Glissade
from model.subscriber import Subscriber
from utils.shared import db
from model.patinoire import Patinoire
from model.arrondissement import Arrondissement
from model.installation_aquatique import InstallationAquatique
from utils.utils import parse_integer
from utils.utils import reformat_ince_rink_xml
from utils.utils import trim_space_in_name
from utils.sender import send_mail
from utils.sender import send_tweet

# List of new installations
new_installations = []


def create_or_update_database():
    """Create or update the app's database."""

    try:
        new_arrondissements = {}
        new_arrondissements["last_id"] = Arrondissement.query.count()
        response = fetch_data()
        ice_rink_raw_xml = response["ice_rink"]
        insert_arrondissement_ice_rinks(ice_rink_raw_xml, new_arrondissements)
        playground_slides_raw_xml = response["playground_slide"]
        insert_playground_slides(
            playground_slides_raw_xml, new_arrondissements
        )

        aquatic_installation_data = response["aquatic_installation"]
        insert_aquatic_installations(
            aquatic_installation_data, new_arrondissements
        )
        insert_arrondissements(new_arrondissements)
        notify_by_mail(new_installations)
        notify_on_twitter(new_installations)
        new_installations.clear()
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
    playground_slide = http.request("GET", playground_slide_url)
    aquatic_installation = http.request("GET", aquatic_installation_url)
    ice_rink = http.request("GET", ice_rink_url)
    response = {
        "playground_slide": playground_slide.data.decode("utf-8"),
        "aquatic_installation": aquatic_installation.data.decode("utf-8"),
        "ice_rink": ice_rink.data.decode("utf-8"),
    }
    return response


def insert_arrondissement_ice_rinks(ice_rink_raw_xml, new_arrondissements):
    """Insert ice rink from xml to app's database"""

    ice_rink_xml = reformat_ince_rink_xml(ice_rink_raw_xml)
    data = xmltodict.parse(ice_rink_xml, dict_constructor=dict)
    arrondissements_data = data["MAIN"]["arrondissement"]
    for arrondissement in arrondissements_data:
        arr_name = trim_space_in_name(arrondissement["nom_arr"])
        arr_id = new_arrondissements["last_id"]
        ice_rinks = arrondissement["patinoire"]
        query = Arrondissement.query.filter(Arrondissement.nom == arr_name)
        result = query.first()
        if result is None:
            arrondissementA = Arrondissement(id=arr_id, nom=arr_name)
            new_arrondissements[arr_name] = arrondissementA
            new_arrondissements["last_id"] += 1
        else:
            arr_id = result.id
        insert_ice_rinks(ice_rinks, arr_id)


def insert_ice_rinks(ice_rinks_list, arrondissement_id):
    """Insert ice rink to app's database"""

    ice_rink_list = []
    for ice_rink in ice_rinks_list:
        query = Patinoire.query.filter(
            Patinoire.nom == ice_rink["nom_pat"],
            Patinoire.arrondissement_id == arrondissement_id,
        )
        result = query.first()
        if result is not None:
            ice_rink_info = create_ice_rink_info(ice_rink)
            update_ice_rink(query, ice_rink_info)
        else:
            ice_rink = Patinoire(ice_rink)
            ice_rink.set_arrondissement_id(arrondissement_id)
            ice_rink_list.append(ice_rink)
            new_installations.append(ice_rink.get_name())
    db.session.add_all(ice_rink_list)
    db.session.commit()
    notify_subscribers_start(ice_rink_list)


def update_ice_rink(query, ice_rink_info):
    """Apply a query to update an ice rink inside the DB"""

    query.update(
        {
            "date_heure": ice_rink_info["date_heure"],
            "ouvert": ice_rink_info["ouvert"],
            "deblaye": ice_rink_info["deblaye"],
            "arrose": ice_rink_info["arrose"],
            "resurface": ice_rink_info["resurface"],
        }
    )


def create_ice_rink_info(ice_rink):
    """Create a simplified ice rink info"""

    ice_rink_info = {}
    ice_rink_condition = ice_rink["condition"]
    last_condition = ice_rink_condition[len(ice_rink_condition) - 1]
    ice_rink_info["date_heure"] = last_condition["date_heure"]
    ice_rink_info["ouvert"] = parse_integer(last_condition["ouvert"])
    ice_rink_info["deblaye"] = parse_integer(last_condition["deblaye"])
    ice_rink_info["arrose"] = parse_integer(last_condition["arrose"])
    ice_rink_info["resurface"] = parse_integer(last_condition["resurface"])
    return ice_rink_info


def insert_playground_slides(playground_slides_raw_xml, new_arrondissements):
    """Insert playground slides into app's database"""

    playground_slides_raw = xmltodict.parse(playground_slides_raw_xml)
    playground_slides = playground_slides_raw["glissades"]["glissade"]
    playground_slide_list = []
    for playground_slide in playground_slides:
        arr_id = update_arrondissement(playground_slide, new_arrondissements)
        query = Glissade.query.filter(
            Glissade.nom == playground_slide["nom"],
            Glissade.arrondissement_id == arr_id,
        )
        result = query.first()
        if result is not None:
            info = create_playground_slide_info(playground_slide)
            update_playground_slide(query, info)
        else:
            playground_slide = Glissade(playground_slide)
            playground_slide.set_arrondissement_id(arr_id)
            playground_slide_list.append(playground_slide)
            new_installations.append(playground_slide.get_name())
    db.session.add_all(playground_slide_list)
    db.session.commit()
    notify_subscribers_start(playground_slide_list)


def update_arrondissement(playground_slide, new_arrondissements):
    """Update arrondissement data and return its id"""

    ps_arr = playground_slide["arrondissement"]
    arr_name_raw = ps_arr["nom_arr"]
    arr_name = trim_space_in_name(arr_name_raw)
    cle_arr = ps_arr["cle"]
    date_maj_arr = ps_arr["date_maj"]
    date_maj = datetime.strptime(date_maj_arr, "%Y-%m-%d %H:%M:%S")
    query = Arrondissement.query.filter(Arrondissement.nom == arr_name)
    result = query.first()
    if result is not None:
        query.update({"cle": cle_arr, "date_maj": date_maj})
        return result.id
    else:
        arr = None
        if new_arrondissements.keys().__contains__(arr_name):
            arr = new_arrondissements[arr_name]
            arr.set_cle(cle_arr)
            arr.set_date_maj(date_maj)
        else:
            arr_id = new_arrondissements["last_id"]
            arr = Arrondissement(id=arr_id, nom=arr_name)
            arr.set_cle(cle_arr)
            arr.set_date_maj(date_maj)
            new_arrondissements[arr_name] = arr
            new_arrondissements["last_id"] += 1
        return arr.get_id()


def create_playground_slide_info(playground_slide):
    """TODO"""

    playground_slide_info = {}
    playground_slide_info["ouvert"] = parse_integer(playground_slide["ouvert"])
    playground_slide_info["deblaye"] = parse_integer(
        playground_slide["deblaye"]
    )
    playground_slide_info["condition"] = playground_slide["condition"]
    return playground_slide_info


def update_playground_slide(query, playground_slide_info):
    """Apply a query to update a playground_slide in the DB"""

    query.update(
        {
            "ouvert": playground_slide_info["ouvert"],
            "deblaye": playground_slide_info["deblaye"],
            "condition": playground_slide_info["condition"],
        }
    )


def insert_aquatic_installations(
    aquatic_installation_data, new_arrondissements
):
    """Insert aquatic installation into app's database"""

    file = StringIO(aquatic_installation_data)
    data = csv.DictReader(file, delimiter=",")
    next(data)
    piscine_list = []
    for row in data:
        arr_id = get_arrondissement(row, new_arrondissements)
        query = InstallationAquatique.query.filter(
            InstallationAquatique.nom == row["NOM"],
            InstallationAquatique.arrondissement_id == arr_id,
            InstallationAquatique.type == row["TYPE"],
        )
        result = query.first()
        if result is not None:
            update_aquatic_installation(query, row)
        else:
            aquatic_installation = InstallationAquatique(row)
            aquatic_installation.set_arrondissement_id(arr_id)
            piscine_list.append(aquatic_installation)
            new_installations.append(aquatic_installation.get_name())
    db.session.add_all(piscine_list)
    db.session.commit()
    notify_subscribers_start(piscine_list)


def get_arrondissement(row, new_arrondissements):
    """Get id of an arrondissement from aquatic_installation_data csv"""

    arr_name = trim_space_in_name(row["ARRONDISSE"])
    arr_id = new_arrondissements["last_id"]
    query = Arrondissement.query.filter(Arrondissement.nom == arr_name)
    result = query.first()
    if result is not None:
        arr_id = result.id
    else:
        if new_arrondissements.keys().__contains__(arr_name):
            arr = new_arrondissements[arr_name]
            arr_id: int = arr.get_id()
        else:
            arr = Arrondissement(id=arr_id, nom=arr_name)
            new_arrondissements[arr_name] = arr
            new_arrondissements["last_id"] += 1
    return arr_id


def update_aquatic_installation(query, row):
    """Apply a query to update a aquatic installation in the DB"""

    query.update(
        {
            "adresse": row["ADRESSE"],
            "propriete": row["PROPRIETE"],
            "gestion": row["GESTION"],
            "equipement": row["EQUIPEME"],
        }
    )


def insert_arrondissements(new_arrondissements):
    """Insert arrondissement into app's database"""

    arrondissements = []
    for key in new_arrondissements:
        if key != "last_id":
            arrondissements.append(new_arrondissements[key])

    db.session.add_all(arrondissements)
    db.session.commit()


def notify_by_mail(new_installations):
    """
    Notify the defined recipient in config by mail about added installations
    """

    body = """
    Bonjour, voici la liste des nouvelles installations que nous avons ajouté
    depuis votre dernière visite:
    """
    if len(new_installations) > 0:
        for installation in new_installations:
            body += f"\n\t- {installation}"
        print(
            f" * Sending email to {config.RECIPIENT} about new installations"
        )
        send_mail(config.RECIPIENT, config.SUBJECT, body)
    else:
        print(" * No new installations. Sending email aborted")


def notify_on_twitter(new_installations):
    """
    Notify on twitter about new added installations
    """

    if len(new_installations) > 0:
        print(" * Publishing updates result on Twitter")
        send_tweet(new_installations)
    else:
        print("No new installations. Sending email aborted")


def notify_subscribers_start(new_facilities):
    """
    Start the process of notifying the subscribers about new facilities
    located in the boroughs they follow.
    The process starts only when the database is updated.

    :param new_facilities: A list of the new facilities added to the database.
    """
    if g.LAST_DATABASE_ACTION == "UPDATE":
        for facility in new_facilities:
            notify_subscribers(facility)


def notify_subscribers(new_facility):
    """
    Search the database for subscribers who follow the borough of a new
    facility added in the database, then send them
    an email.

    :param new_facility: The new facility
    """
    borough_id = new_facility.arrondissement_id
    subscribers = Subscriber.query.all()
    for subscriber in subscribers:
        for borough in subscriber.boroughs_to_follow:
            if borough == borough_id:
                notify_subscriber_by_mail(subscriber, new_facility)


def notify_subscriber_by_mail(subscriber, facility):
    """
    Send an email to a subscriber about a new facility added in a borough
    he follow.

    :param subscriber: The subscriber to send the email
    :param facility: The facility to be mentioned in the email
    """
    new_facility_borough = Arrondissement.query.filter(
        Arrondissement.id == facility.arrondissement_id
    ).first()
    mail_body = render_template(
        "new_facility_in_borough_email.html",
        subscriber=subscriber,
        facility=facility,
        borough=new_facility_borough,
    )
    send_mail(subscriber.email, "Nouvelle installation disponible", mail_body)
