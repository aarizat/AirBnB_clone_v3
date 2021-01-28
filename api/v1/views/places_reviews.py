#!/usr/bin/python3
"""
a new view for Review objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('places/<place_id>/reviews', methods=["GET", "POST"],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a place
    Create a new Review object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        reviews = storage.all(Review).values()
        return jsonify([review.to_dict() for review in reviews
                        if review.place_id == place_id])
    if request.method == "POST":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        elif "user_id" not in body:
            abort(400, "Missing user_id")
        user = storage.get(User, body["user_id"])
        if user is None:
            abort(404)
        elif "text" not in body:
            abort(400, "Missing text")
        else:
            body["place_id"] = place_id
            obj = Review(**body)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201


@app_views.route('reviews/<review_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        body = request.get_json(silent=True)
        if body is None:
            abort(400, "Not a JSON")
        for k, v in body.items():
            if k not in ['id', 'user_id', 'place_id',
                         'created_at', 'updated_at']:
                setattr(review, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200
