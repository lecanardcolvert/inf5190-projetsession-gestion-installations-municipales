from flask import Flask, render_template
from datetime import datetime

from utils.shared import db
from routes.router import router
from config import Config
from model.arrondissement import Arrondissement

# App configurations
app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(Config)

# Initialization
db.init_app(app)

# Register blueprints
app.register_blueprint(router)

# Create database if doesn't exist yet
with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html')


if '__main__' == __name__:
    app.run(debug=True)
