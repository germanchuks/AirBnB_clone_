#!/usr/bin/python3
"""Defines city endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [obj.to_dict() for obj in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_with_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    return (jsonify(city.to_dict()) if city else abort(404))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_with_id(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = get_json_data()
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object."""
    city = storage.get(City, city_id)
    if city:
        data = get_json_data()
        ignore_keys = ['id', 'created_at', 'updated_at']
        [setattr(city, key, value) for key, value in data.items()
         if key not in ignore_keys]
        city.save()
        return make_response(jsonify(city.to_dict()), 200)
    else:
        abort(404)
