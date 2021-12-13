# Native and installed modules
import os
from flask import Blueprint, current_app, render_template

router = Blueprint("router", __name__)


@router.route('/')
def home():
    return render_template('index.html')


@router.route('/doc')
def doc():
    input_raml = os.path.join(current_app.root_path, 'api', 'api.raml')
    output_html = os.path.join(current_app.root_path,
                               current_app.static_folder, 'html',
                               'api-doc.html')
    os.system("raml2html " + input_raml + " > " + output_html)
    return current_app.send_static_file('html/api-doc.html')
