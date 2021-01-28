#!/usr/bin/python3
"""
a new view for State objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, redirect, url_for, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def return_all_amenities():
    """
    Retrieves the list of all State objects
    """
    amen_lst = storage.all(Amenity)
    amen_dict = [amenities.to_dict() for amenities in amen_lst.values()]
    return jsonify(amen_dict)


@app_views.route('amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def return_amen_by_id(amenity_id):
    """
    returnsamenities by id
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_object_amen(amenity_id):
    """
    delete and object base on his id
    """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def add_amenity_by_header():
    """
    create a new object according to the header parameters
    """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    elif "name" not in body:
        abort(400, "Missing name")
    else:
        obj = Amenity(**body)
        storage.new(obj)
        storage.save()
        return jsonify(storage.get(Amenity, obj.id).to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity_by_header(amenity_id):
    """
    update the name of an object
    """
    body = request.get_json(silent=True)
    if body is None:
        abort(400, "Not a JSON")
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    if "name" in body:
        obj.name = body['name']
        storage.save()
    return jsonify(obj.to_dict()), 200
