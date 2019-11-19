from flask import Flask

from unitext import convert


def create_app():
    app = Flask(__name__)

    app.register_blueprint(convert.bp)

    return app
