#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API
actions
"""

from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage

cls = Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
@app_views.route("/amenities/<string:amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Retrieves a Amenity object"""
    if amenity_id is not None:
        obj = storage.get(cls, amenity_id)
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


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        storage.reload()
        return jsonify({})


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    if "name" not in my_dict:
        abort(400, "Missing name")
    names = my_dict["name"]
    obj = cls(name=names)
    storage.new(obj)
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        abort(404)
    my_dict = request.get_json(silent=True)
    if my_dict is None:
        abort(400, "Not a JSON")
    for k, v in my_dict.items():
        if k == 'id' or k == 'created_at' or k == 'updated_at':
            continue
        setattr(obj, k, v)
    obj.save()
    storage.save()
    storage.reload()
    return jsonify(obj.to_dict()), 200
