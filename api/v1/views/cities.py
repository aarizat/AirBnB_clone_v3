#!/usr/bin/python3
"""
a new view for City objects that handles all default RestFul API actions.
"""
from flask import abort, jsonify
from flask import request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('states/<state_id>/cities', methods=["GET", "POST"],
                 strict_slashes=False)
def cities_by_state(state_id):
    """
    Retrieve all of cities that matches with stated_id.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = storage.all(City).values()
        return jsonify([city.to_dict() for city in cities
                        if city.state_id == state_id])
    if request.method == "POST":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        elif "name" not in body:
            abort(400, "Missing name")
        else:
            obj = City(**body)
            storage.new(obj)
            storage.save()
            return jsonify(storage.get(City, obj.id).to_dict()), 201


@app_views.route('cities/<city_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        elif "name" in body:
            city.name = body['name']
            storage.save()
        return jsonify(city.to_dict()), 200
