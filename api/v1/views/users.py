#!/usr/bin/python3
"""
a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, redirect, url_for, request, abort
from models.user import User
from models import storage
import hashlib


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def return_all_users():
    """
    Retrieves the list of all State objects
    """
    usr_lst = storage.all(User)
    usr_dict = [user.to_dict() for user in usr_lst.values()]
    return jsonify(usr_dict)


@app_views.route('users/<user_id>', methods=["GET"],
                 strict_slashes=False)
def return_usr_by_id(user_id):
    """
    returnsamenities by id
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_object_usr(user_id):
    """
    delete and object base on his id
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def add_usr_by_header():
    """
    create a new object according to the header parameters
    """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    elif "email" not in body:
        abort(400, "Missing email")
    elif "password" not in body:
        abort(400, "Missing password")
    else:
        obj = User(**body)
        storage.new(obj)
        storage.save()
        return jsonify(storage.get(User, obj.id).to_dict()), 201


@app_views.route('/users/<user_id>', methods=["PUT"],
                 strict_slashes=False)
def update_usr_by_header(user_id):
    """
    update the name of an object
    """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in body.items():
        if key == "password":
            value = hashlib.md5(value.encode("utf-8")).hexdigest()
        if key not in ("id", "email", "created_at", "updated_at"):
            setattr(obj, key, value)
    storage.save()
    return jsonify(storage.get(User, user_id).to_dict()), 200
