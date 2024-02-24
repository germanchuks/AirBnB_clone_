#!/usr/bin/python3
"""Defines amenity endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
import os


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_for_place(place_id):
    """Retrieves the list of all Amenity objects of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        amenities = [obj.to_dict() for obj in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes an Amenity associated with a Place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not (place and amenity):
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not (place and amenity):
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify({amenity.to_dict()}), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify({amenity.to_dict()}), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify({}), 201
