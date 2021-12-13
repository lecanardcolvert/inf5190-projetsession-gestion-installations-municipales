# Native and installed modules
from flask import Blueprint, current_app, render_template

router = Blueprint("router", __name__)


@router.route("/")
def home():
    return render_template("index.html")


@router.route("/doc")
def doc():
    return render_template("api-doc.html")
