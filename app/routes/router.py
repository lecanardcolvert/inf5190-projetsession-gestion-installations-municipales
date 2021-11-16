from flask import Blueprint

router = Blueprint("router", __name__)


@router.route('/')
def home():
    return "Hello, world! from Victor Ziguehi"
