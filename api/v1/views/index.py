#!/usr/bin/python3
"""
flask app for the AirBnB project
"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    """Returns status in JSON format"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """retrieves the number of each objects by type"""
    objs = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(objs)
