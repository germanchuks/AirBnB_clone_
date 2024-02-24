#!/usr/bin/python3
"""Main module for AirBnB Clone API"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable CORS for all routes under "/api/" and requests from "0.0.0.0"
CORS(app, resources={r'/api/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the database."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
