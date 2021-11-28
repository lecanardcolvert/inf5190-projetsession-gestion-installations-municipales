from flask import Flask, render_template

from api.api import api
from config import Config
from routes.router import router
from utils.shared import db

# App configurations
app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialization
db.init_app(app)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(router)

# Create database if doesn't exist yet
with app.app_context():
    db.create_all()
    # À REMETTRE AVANT DE PUSH
    # update_database()


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run(debug=True)
