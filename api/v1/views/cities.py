#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from flask import jsonify, abort, request
from models import storage

cls = City


@app_views.route("/states/<string:state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_city_state(state_id):
    """Retrieves the list of all City objects of a State"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    cities = []
    for city in obj.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<string:city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id=None):
    """Retrieves a City object"""
    if city_id is not None:
        obj = storage.get(cls, city_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        objs = storage.all(cls)
        my_lst = []
        for obj in objs.values():
            my_lst.append(obj.to_dict())
        return jsonify(my_lst)


@app_views.route("/cities/<string:city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    obj = storage.get(cls, city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id=None):
    """Creates a City"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "name" not in my_dict:
        abort(400, "Missing name")
    names = my_dict["name"]
    obj = cls(name=names, state_id=state_id)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def update_city(city_id):
    """Updates a City object"""
    obj = storage.get(cls, city_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'updated_at' or k == 'state_id':
            continue
        if k == 'id' or k == 'created_at':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
