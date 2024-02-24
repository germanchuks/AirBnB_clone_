#!/usr/bin/python3
"""Defines review endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [obj.to_dict() for obj in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_with_id(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    return (jsonify(review.to_dict()) if review else abort(404))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_with_id(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = get_json_data()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    # Check if user_id is linked to any existing User object
    if not storage.get(User, data['user_id']):
        abort(404)

    if 'text' not in data:
        abort(400, 'Missing text')

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object."""
    review = storage.get(Review, review_id)
    if review:
        data = get_json_data()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        [setattr(review, key, value) for key, value in data.items()
         if key not in ignore_keys]
        review.save()
        return make_response(jsonify(review.to_dict()), 200)
    else:
        abort(404)
