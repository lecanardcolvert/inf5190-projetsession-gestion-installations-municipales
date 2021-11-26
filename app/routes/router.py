import os
from flask import Blueprint, current_app, render_template

router = Blueprint("router", __name__)


@router.route('/')
def home():
    return render_template('index.html')


@router.route('/doc')
def doc():
    os.system("raml2html ./api/api.raml > ./static/html/api-doc.html")
    return current_app.send_static_file('html/api-doc.html')
