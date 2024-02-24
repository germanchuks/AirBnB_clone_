#!/usr/bin/python3
"""Defines place endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


def get_json_data():
    """Helper function to get JSON data from the request."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    return data


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [obj.to_dict() for obj in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_with_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    return (jsonify(place.to_dict()) if place else abort(404))


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_with_id(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = get_json_data()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    # Check if user_id is linked to any existing User object
    if not storage.get(User, data['user_id']):
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place:
        data = get_json_data()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        [setattr(place, key, value) for key, value in data.items()
         if key not in ignore_keys]
        place.save()
        return make_response(jsonify(place.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Retrieves all Place objects depending of the JSON in the body of the
    request"""
    data = get_json_data()

    if not data or not any(data.values()):
        places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(places)

    list_places = []

    states = data.get('states', [])
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                list_places.extend(city.places)

    cities = data.get('cities', [])
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            list_places.extend(city.places)

    list_places = list(set(list_places))

    amenities = data.get('amenities', [])
    if amenities:
        amenities_obj = [storage.get(Amenity, amenity_id)
                         for amenity_id in amenities]
        list_places = [place for place in list_places
                       if all(amenity in place.amenities
                              for amenity in amenities_obj)]

    places = [place.to_dict(exclude=['amenities']) for place in list_places]
    return jsonify(places)
