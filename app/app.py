from flask import Flask
from routes.router import router

app = Flask(__name__, static_folder="static", static_url_path="/")
app.register_blueprint(router)

if '__main__' == __name__:
    app.run()
