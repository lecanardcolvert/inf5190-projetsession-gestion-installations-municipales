# Native and installed modules
from flask import Blueprint, render_template
from model.arrondissement import Arrondissement, ArrondissementModel
from model.glissade import Glissade
from model.patinoire import Patinoire
from model.installation_aquatique import InstallationAquatique
from utils.utils import login_required
import config

router = Blueprint("router", __name__)


@router.route("/")
def home():
    return render_template("index.html")


@router.route("/doc")
def doc():
    return render_template("api-doc.html")


@router.route("/subscribe", methods=["GET"])
def subscribe():
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    return render_template("subscribe.html", boroughs=serialized_boroughs)


@router.route("/subscribe-success", methods=["GET"])
def subscribe_success():
    return render_template("subscribe-success.html")


@router.route("/installations/playground-slides/<id>/edit", methods=["GET"])
@login_required
def edit_playgroud_slide(id):
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    playground_slide = Glissade.query.get(id)
    return render_template(
        "edit_playground_slide.html",
        boroughs=serialized_boroughs,
        id=id,
        nom=playground_slide.nom,
        ouvert=playground_slide.ouvert,
        deblaye=playground_slide.deblaye,
        condition=playground_slide.condition,
    )


@router.route("/installations/ice-rinks/<id>/edit", methods=["GET"])
@login_required
def edit_ice_rink(id):
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    ice_rink = Patinoire.query.get(id)
    return render_template(
        "edit_ice_rink.html",
        boroughs=serialized_boroughs,
        id=id,
        nom=ice_rink.nom,
        ouvert=ice_rink.ouvert,
        deblaye=ice_rink.deblaye,
        resurface=ice_rink.resurface,
        date_heure=ice_rink.date_heure,
        arrose=ice_rink.arrose,
    )


@router.route("/installations/aquatics/<id>/edit", methods=["GET"])
@login_required
def edit_aquatic_installation(id):
    borough_list = Arrondissement.query.all()
    borough_model = ArrondissementModel(many=True)
    serialized_boroughs = borough_model.dump(borough_list)
    aquatic_installation = InstallationAquatique.query.get(id)
    return render_template(
        "edit_aquatic_installation.html",
        boroughs=serialized_boroughs,
        id=id,
        nom=aquatic_installation.nom,
        type=aquatic_installation.type,
        adresse=aquatic_installation.adresse,
        propriete=aquatic_installation.propriete,
        gestion=aquatic_installation.gestion,
        equipement=aquatic_installation.equipement,
    )
