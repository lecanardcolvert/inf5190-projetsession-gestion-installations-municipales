# Native and installed modules
import atexit
import os
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, g

# Custom modules
import config
from api.api import api
from routes.router import router
from utils.shared import db
from utils.update_database import create_or_update_database

# App configurations
app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(config.config["development"])
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

# Auto update config
update_job = BackgroundScheduler({"apscheduler.timezone": "America/Toronto"})
update_job.add_job(
    lambda: update_database(),
    "cron",
    day="*",
    hour="0",
    minute="00",
)
update_job.start()
atexit.register(lambda: update_job.shutdown(wait=False))

# Initialization
db.init_app(app)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(router)

# Create database if it doesn't exist yet
with app.app_context():
    if not os.path.isfile(config.DB_PATH):
        print(" * CREATING DATABASE")
        g.LAST_DATABASE_ACTION = "CREATE"
        db.create_all()
        create_or_update_database()
        print(" * CREATION FINISHED")


def update_database():
    with app.app_context():
        print(" * UPDATING DATABASE")
        g.LAST_DATABASE_ACTION = "UPDATE"
        create_or_update_database()
        print(" * UPDATE FINISHED")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run(debug=True)
