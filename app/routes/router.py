import flask
from flask import Blueprint, render_template

router = Blueprint("router", __name__)


@router.route('/')
def home():
    return render_template('index.html')


@router.route('/doc')
def doc():
    return flask.Response(status=501)
