#!/usr/bin/python3
"""
Create app Flask
"""
from flask_cors import CORS
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(exc):
    """
    Close session database.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    Manage not found error.
    """
    return {"error": "Not found"}, 404

if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST"), port=getenv("HBNB_API_PORT"))
