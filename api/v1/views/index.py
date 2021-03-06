#!/usr/bin/python3
"""
Display status code.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State


@app_views.route("/status")
def display_status():
    """
    Return status code OK
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def display_count():
    """
    Return the count of objects by type
    """
    return {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        }
