#!/usr/bin/python3
"""Defines state endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_state_objs = storage.all(State).values()
    state_objs_dict = [obj.to_dict() for obj in all_state_objs]
    return jsonify(state_objs_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_with_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    return (jsonify(state.to_dict()) if state else abort(404))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_with_id(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State."""
    data = get_json_data()
    if 'name' not in data:
        abort(400, 'Missing name')

    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if state:
        data = get_json_data()
        ignore_keys = ['id', 'created_at', 'updated_at']
        [setattr(state, key, value) for key, value in data.items()
         if key not in ignore_keys]
        state.save()
        return make_response(jsonify(state.to_dict()), 200)
    else:
        abort(404)
