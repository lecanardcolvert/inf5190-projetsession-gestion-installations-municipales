from flask import Flask, render_template
from routes.router import router

app = Flask(__name__, static_folder="static", static_url_path="/")
app.register_blueprint(router)

if '__main__' == __name__:
    app.run()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html')