#!/usr/bin/python3
"""
a new view for Review objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Review objects of a place
    Create a new Review object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        list_res = place.amenities
    else:
        list_res = place.amenity_ids
    return jsonify([amenity.to_dict() for amenity in list_res])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=["DELETE", "POST"],
                 strict_slashes=False)
def delete_post_amenity_place(place_id, amenity_id):
    """Retrieves a Review object
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if request.method == "DELETE":
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            list_res = place.amenities
        else:
            list_res = place.amenity_ids
        if amenity not in list_res:
            abort(404)
        list_res.remove(amenity)
        place.save()
        return jsonify({}), 200
    if request.method == "POST":
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            list_res = place.amenities
        else:
            list_res = place.amenity_ids
        if amenity not in list_res:
            list_res.append(amenity)
            place.save()
            return jsonify(amenity.to_dict()), 201
        return jsonify(amenity.to_dict()), 200
