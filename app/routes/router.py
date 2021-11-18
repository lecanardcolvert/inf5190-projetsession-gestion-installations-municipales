from flask import Blueprint, render_template

router = Blueprint("router", __name__)


@router.route('/')
def home():
    return render_template('index.html')