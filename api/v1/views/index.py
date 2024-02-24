#!/usr/bin/python3
"""Defines Blueprint endpoints for the AirBnB Clone v1 API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response."""
    resp = {'status': 'OK'}
    return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Retrieves the number of each objects by type."""
    obj_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
        }
    return jsonify(obj_stats)
