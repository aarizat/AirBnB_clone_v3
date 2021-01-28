#!/usr/bin/python3
"""
a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, redirect, url_for, request, abort
from models.state import State
from models import storage
from models.base_model import BaseModel


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def return_all_states():
    """
    Retrieves the list of all State objects
    """
    states_lst = storage.all(State)
    states_dict = [states.to_dict() for states in states_lst.values()]
    return jsonify(states_dict)


@app_views.route('states/<state_id>', methods=["GET"], strict_slashes=False)
def return_state_by_id(state_id):
    """
    Return and state object by Id
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_object(state_id):
    """
    Delete an object by id
    """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def add_state_by_header():
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body:
        abort(400, "Missing name")
    else:
        obj = State(**body)
        storage.new(obj)
        storage.save()
        return jsonify(storage.get(State, obj.id).to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_state_by_header(state_id):
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if "name" in body:
        obj.name = body['name']
        storage.save()
    return jsonify(obj.to_dict()), 200
