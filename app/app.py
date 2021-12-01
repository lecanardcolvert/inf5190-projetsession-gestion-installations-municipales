import atexit
from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from utils.shared import db
from routes.router import router
from config import Config
from utils.update_database import update_database

# App configurations
app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(Config)

# Auto update config
update_job = BackgroundScheduler()
update_job.add_job(
    lambda: update_database(), "cron", day="*", hour="01", minute="7"
)
update_job.start()
atexit.register(lambda: update_job.shutdown(wait=False))
# Initialization
db.init_app(app)

# Register blueprints
app.register_blueprint(router)

# Create database if doesn't exist yet
with app.app_context():
    db.create_all()
    update_database()


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run(debug=True)
