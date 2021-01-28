#!/usr/bin/python3
"""
a new view for Place objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    Create a new Place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places
                        if place.city_id == city_id])
    if request.method == "POST":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        elif "user_id" not in body:
            abort(400, "Missing user_id")
        user = storage.get(User, body["user_id"])
        if user is None:
            abort(404)
        elif "name" not in body:
            abort(400, "Missing name")
        else:
            body["city_id"] = city_id
            obj = Place(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201


@app_views.route('places/<place_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a City object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        _dict = {k: v for k, v in body.items() if k not in
                 ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
                 }
        obj = Place(**_dict)
        storage.save()
        return jsonify(obj.to_dict()), 200
