#!/usr/bin/python3
"""Defines amenity endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    all_amenity_objs = storage.all(Amenity).values()
    amenity_objs_dict = [obj.to_dict() for obj in all_amenity_objs]
    return jsonify(amenity_objs_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_with_id(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    return (jsonify(amenity.to_dict()) if amenity else abort(404))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_with_id(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity."""
    data = get_json_data()
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = get_json_data()
        ignore_keys = ['id', 'created_at', 'updated_at']
        [setattr(amenity, key, value) for key, value in data.items()
         if key not in ignore_keys]
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        abort(404)
