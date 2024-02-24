#!/usr/bin/python3
"""Defines user endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_user_objs = storage.all(User).values()
    user_objs_dict = [obj.to_dict() for obj in all_user_objs]
    return jsonify(user_objs_dict)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_with_id(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    return (jsonify(user.to_dict()) if user else abort(404))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_with_id(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User."""
    data = get_json_data()
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if user:
        data = get_json_data()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        [setattr(user, key, value) for key, value in data.items()
         if key not in ignore_keys]
        user.save()
        return make_response(jsonify(user.to_dict()), 200)
    else:
        abort(404)
