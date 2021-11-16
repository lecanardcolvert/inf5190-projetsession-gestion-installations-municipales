from flask import Flask

app = Flask(__name__, static_folder="static", static_url_path="/")


@app.route('/')
def home():
    return "Hello, world! from Victor Ziguehi"


if '__main__' == __name__:
    app.run
