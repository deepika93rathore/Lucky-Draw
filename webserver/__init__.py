import os
from flask import Flask, json
from werkzeug.exceptions import HTTPException
from webserver.views.lucky_draw import lucky_draw_bp


def create_app(debug=None):
    """ Generate a Flask app with all configurations done and connections established.
    In the Flask app returned, blueprints are registered.
    """
    app = Flask(import_name=__name__)

    if debug is not None:
        app.debug = debug

    _register_blueprints(app)
    return app


def _register_blueprints(app):
    """ Register blueprints for the given Flask app. """
    app.register_blueprint(lucky_draw_bp, url_prefix="/lucky-draw")
